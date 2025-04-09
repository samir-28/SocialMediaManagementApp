from rest_framework import viewsets, generics, permissions ,status 
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Like, Follow, Notification
from .serializers import NotificationSerializer, ProfileSerializer, PostSerializer, CommentSerializer
from rest_framework.views import APIView
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny 
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Get the data from the request
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, password=password, email=email)

        # Create the profile linked to the user
        Profile.objects.create(user=user)

        # Return a success response
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only access their own profile
        return Profile.objects.filter(user=self.request.user)
    
    
    
    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()

        # Delete the associated user account
        user = profile.user
        user.delete()  # This will delete the User instance

        # Delete the profile
        profile.delete()

        # Return a 204 No Content response after deletion
        return Response(status=status.HTTP_204_NO_CONTENT)


# List and create posts for all users, but only logged-in users can perform CRUD on their posts.
class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        # Set the user to the logged-in user
        post = serializer.save(user=self.request.user)
        # Notify followers about the new post
        followers = Follow.objects.filter(followed=self.request.user)
        for f in followers:
            Notification.objects.create(user=f.follower, text=f'{self.request.user.username} created a new post')


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure a user can only edit/delete their own post
        return Post.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        # Ensure the user is the owner of the post before updating
        post = serializer.save()
        return post

    def perform_destroy(self, instance):
        # Ensure the user is the owner of the post before deleting
        instance.delete()


# Like functionality (users can like/unlike a post)
class PostLikeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        post = Post.objects.get(id=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({'msg': 'Unliked'})
        
        # Create a notification when the post is liked
        Notification.objects.create(user=post.user, text=f'{request.user.username} liked your post')
        return Response({'msg': 'Liked'})


class PostCommentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer  # Adding the serializer_class

    def post(self, request, pk=None):
        # Get the post object by its ID
        post = Post.objects.get(id=pk)
        
        # Get comment text from request data
        comment_text = request.data.get('text')

        if not comment_text:
            return Response({'error': 'Comment text is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new comment
        comment = Comment.objects.create(user=request.user, post=post, text=comment_text)
        
        # Create a notification for the post author
        Notification.objects.create(user=post.user, text=f'{request.user.username} commented on your post')
        
        # Return the serialized comment data
        return Response(self.serializer_class(comment).data)

    def delete(self, request, pk=None):
        # Get the post object by its ID
        post = Post.objects.get(id=pk)
        
        # Get the comment_id from request data
        comment_id = request.data.get('comment_id')

        # Try to find the comment
        comment = Comment.objects.filter(id=comment_id, user=request.user).first()
        
        if comment:
            # Delete the comment if found
            comment.delete()
            return Response({'msg': 'Comment deleted'})
        
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk=None):
        # Get the post object by its ID
        post = Post.objects.get(id=pk)
        
        # Get all comments related to the post
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        
        # Serialize and return the comments
        return Response(self.serializer_class(comments, many=True).data)

    def get(self, request, pk=None):
        # Get the post object by its ID
        post = Post.objects.get(id=pk)
        
        # Get all comments related to the post
        comments = Comment.objects.filter(post=post)
        
        # Serialize and return the comments
        return Response(self.serializer_class(comments, many=True).data)


# Admin Post Deletion using generics.DestroyAPIView
class AdminPostDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Post.objects.all()
    
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response({'msg': 'Post deleted by admin'})


# Follow View (Follow/Unfollow using generics)
class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        followed = User.objects.get(id=pk)
        # Create a follow relationship
        Follow.objects.get_or_create(follower=request.user, followed=followed)
        return Response({'msg': 'Followed'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        followed = User.objects.get(id=pk)
        # Delete the follow relationship
        follow_instance = Follow.objects.filter(follower=request.user, followed=followed).first()
        
        if follow_instance:
            follow_instance.delete()
            return Response({'msg': 'Unfollowed'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Follow relationship not found'}, status=status.HTTP_404_NOT_FOUND)

class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # Return notifications for the currently authenticated user
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
from django.urls import path, include
from .views import  NotificationListView, RegisterView,ProfileDetailView,AdminPostDeleteView, FollowView
from .views import PostListView, PostDetailView, PostLikeView, PostCommentView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/',ProfileDetailView.as_view(), name='profile-detail'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    path('posts/<int:pk>/comment/', PostCommentView.as_view(), name='post-comment'),
    path('admin/posts/<int:pk>/', AdminPostDeleteView.as_view(), name='admin-post-delete'),
    path('follow/<int:pk>/', FollowView.as_view(), name='follow-user'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
]

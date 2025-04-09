from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Post
from rest_framework.test import APIClient

class SocialMediaTestCase(TestCase):
    def setUp(self):
        # Create 5 users and their profiles
        self.users = []
        for i in range(1, 6):
            user = User.objects.create_user(username=f'user{i}', password='password123', email=f'user{i}@example.com')
            profile = Profile.objects.create(user=user)
            self.users.append(user)

        # Create 2 posts for each user
        self.posts = []
        for user in self.users:
            for i in range(1, 3):
                post = Post.objects.create(user=user, content=f'Post {i} for {user.username}')
                self.posts.append(post)

        # Create an API client for testing
        self.client = APIClient()

    
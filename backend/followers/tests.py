"""Contains tests for the follower app."""

from django.test import TestCase
from django.contrib.auth.models import User
from author.models import Author
from followers.models import FriendRequest


class FriendRequestModelTestCase(TestCase):
    """Test cases for the FriendRequest model."""
    def setUp(self) -> None:
        user = User.objects.create_user(username='testuser1', password='12345')
        self.author = Author.objects.create(user=user, host="http://testserver", displayName="Test User 1",
                                            github="github/test1.com", profileImage="profile/test1.com")
        user2 = User.objects.create_user(username='testuser2', password='12345')
        self.author2 = Author.objects.create(user=user2, host="http://testserver", displayName="Test User 2",
                                                github="github/test2.com", profileImage="profile/test2.com")
        FriendRequest.objects.create(type="Follow", summary="Test User 1 wants to follow Test User 2",
                            actor=self.author, object=self.author2)

    def test_friend_request_creation(self):
        """Test that a friend request can be created."""
        author1_friend_requests = FriendRequest.objects.filter(actor=self.author)
        self.assertEqual(author1_friend_requests.count(), 1)
        author2_friend_requests = FriendRequest.objects.filter(actor=self.author2)
        self.assertEqual(author2_friend_requests.count(), 0)

    def test_friend_request_unique(self):
        """Test that a friend request can only be made once."""
        pass

    def test_friend_request_summary(self):
        """Test that a friend request has a summary."""
        pass

    def test_friend_request_actor(self):
        """Test that a friend request has an actor."""
        pass

    def test_friend_request_object(self):
        """Test that a friend request has an object."""
        pass

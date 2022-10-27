"""Contains tests for the follower app."""

from django.test import TestCase
from django.contrib.auth.models import User
from author.models import Author
from followers.models import FriendRequest
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from .views import FollowerList, FollowerDetail

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

class FollowersModelTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create_user(username='testuser1', password='12345')
        Author.objects.create(user=u1, host="http://testserver", displayName="Test User 1",
                              github="github/test1.com", profileImage="profile/test1.com")
        
        u2 = User.objects.create_user(username='testuser2', password='12345')
        Author.objects.create(user=u2, host="http://testserver", displayName="Test User 2",
                              github="github/test2.com", profileImage="profile/test2.com")

    def test_followers_model(self):
        author = Author.objects.get(user__username='testuser1')
        self.assertEqual(author.followers.count(), 0)
        author2 = Author.objects.get(user__username='testuser2')
        author.followers.add(author2)
        self.assertEqual(author.followers.count(), 1)
        self.assertEqual(author.followers.first(), author2)
        #self.assertEqual(author2.following.count(), 1)
        #self.assertEqual(author2.following.first(), author)

class FollowersListViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser1', password='12345')
        self.author = Author.objects.create(user=self.user, host="http://testserver", displayName="Test User 1",
                              github="github/test1.com", profileImage="profile/test1.com")
        self.client.force_authenticate(user=self.user)

        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.author2 = Author.objects.create(user=self.user2, host="http://testserver", displayName="Test User 2",
                                github="github/test2.com", profileImage="profile/test2.com")

        self.author.followers.add(self.author2)

    def test_followers_detail_view_get(self):
        request = self.factory.get('/authors/' + str(self.author.id) + '/followers/', format='json')
        response = FollowerList.as_view()(request, author_id = self.author.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "followers")
        self.assertEqual(response.data["items"][0]["type"], "author")
        self.assertEqual(response.data["items"][0]["id"], str(self.author2.id))
        self.assertEqual(response.data["items"][0]["url"], "http://testserver/authors/" + str(self.author.id)) # should it start with None?
        self.assertEqual(response.data["items"][0]["host"], "http://testserver")
        self.assertEqual(response.data["items"][0]["displayName"], "Test User 1")
        self.assertEqual(response.data["items"][0]["github"], "github/test1.com")
        self.assertEqual(response.data["items"][0]["profileImage"], "profile/test1.com")

class FollowersDetailViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser1', password='12345')
        self.author = Author.objects.create(user=self.user, host="http://testserver", displayName="TestAuthor1",
                              github="github/test1.com", profileImage="profile/test1.com")
        self.client.force_authenticate(user=self.user)

        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.author2 = Author.objects.create(user=self.user2, host="http://testserver", displayName="TestAuthor2",
                                github="github/test2.com", profileImage="profile/test2.com")
    
    def test_followers_detail_view_get(self):
        # test given author 2 is not following author 1
        request = self.factory.get('/authors/' + str(self.author.id) + '/followers/' + str(self.author2.id), format='json')
        response = FollowerDetail.as_view()(request, author_id = self.author.id, foreign_id=self.author2.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "follower")
        self.assertEqual(response.data["detail"], "Foreign author is not following the author.")
        
        # test given author 2 is following author 1
        self.author.followers.add(self.author2)
        request = self.factory.get('/authors/' + str(self.author.id) + '/followers/' + str(self.author2.id), format='json')
        response = FollowerDetail.as_view()(request, author_id = self.author.id, foreign_id=self.author2.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "follower")
        self.assertEqual(response.data["id"], str(self.author2.id))
        self.assertEqual(response.data["url"], "http://testserver/authors/" + str(self.author2.id)) # should it start with None?
        self.assertEqual(response.data["host"], "http://testserver")
        self.assertEqual(response.data["displayName"], "TestAuthor2")
        self.assertEqual(response.data["github"], "github/test2.com")
        self.assertEqual(response.data["profileImage"], "profile/test2.com")

    def test_followers_detail_view_delete(self):
        request = self.factory.delete('/authors/' + str(self.author.id) + '/followers/' + str(self.author2.id), format='json')
        response = FollowerDetail.as_view()(request, author_id = self.author.id, foreign_id=self.author2.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "follower")
        self.assertEqual(response.data["detail"], "Foreign author TestAuthor2 is no longer following the author TestAuthor1.")

    def test_followers_detail_view_put(self):
        request = self.factory.put('/authors/' + str(self.author.id) + '/followers/' + str(self.author2.id), format='json')
        response = FollowerDetail.as_view()(request, author_id = self.author.id, foreign_id=self.author2.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "follower")
        self.assertEqual(response.data["detail"], "Foreign author TestAuthor2 is now following the author TestAuthor1.")    

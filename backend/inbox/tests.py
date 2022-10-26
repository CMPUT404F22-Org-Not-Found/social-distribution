"""Contains the tests for the Inbox app."""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase, APIRequestFactory

from author.models import Author
from post.models import Post
from followers.models import FriendRequest
from inbox.models import Inbox
from inbox.views import InboxView


class InboxModelTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create_user(username='testuser1', password='12345')
        author = Author.objects.create(user=u1, host="http://testserver", displayName="Test User 1",
                              github="github/test1.com", profileImage="profile/test1.com")
        Inbox.objects.create(author=author)

    def test_inbox_model(self):
        inbox = Inbox.objects.get(author__user__username='testuser1')
        self.assertEqual(inbox.type, "inbox")
        self.assertEqual(inbox.author.displayName, "Test User 1")
        self.assertEqual(inbox.author.github, "github/test1.com")
        self.assertEqual(inbox.author.profileImage, "profile/test1.com")
        self.assertEqual(inbox.author.host, "http://testserver")
        self.assertEqual(inbox.author.url, "http://testserver/authors/" + str(inbox.author.id))

    def test_inbox_model_str(self):
        inbox = Inbox.objects.get(author__user__username='testuser1')
        self.assertEqual(str(inbox), "Inbox of Test User 1 - " + str(inbox.author.id))

    def test_inbox_model_posts(self):
        inbox = Inbox.objects.get(author__user__username='testuser1')
        self.assertEqual(inbox.posts.count(), 0)
        post = Post.objects.create(title="Test Post 1", source="http://testserver", origin="http://testserver",
                                   description="Test Post 1 Description", contentType="text/plain",
                                   content="Test Post 1 Content", author=inbox.author)
        inbox.posts.add(post)
        self.assertEqual(inbox.posts.count(), 1)
        self.assertEqual(inbox.posts.first(), post)

    def test_inbox_model_friend_requests(self):
        inbox = Inbox.objects.get(author__user__username='testuser1')
        self.assertEqual(inbox.friend_requests.count(), 0)
        u2 = User.objects.create_user(username='testuser2', password='12345')
        author2 = Author.objects.create(user=u2, host="http://testserver", displayName="Test User 2",
                              github="github/test2.com", profileImage="profile/test2.com")
        friend_request = FriendRequest.objects.create(actor=author2, object=inbox.author)
        inbox.friend_requests.add(friend_request)
        self.assertEqual(inbox.friend_requests.count(), 1)
        self.assertEqual(inbox.friend_requests.first(), friend_request)


class InboxViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.u1 = User.objects.create_user(username='testuser1', password='12345')
        self.author = Author.objects.create(user=self.u1, host="http://testserver", displayName="Test User 1",
                              github="github/test1.com", profileImage="profile/test1.com")
        self.inbox = Inbox.objects.create(author=self.author)
        self.u2 = User.objects.create_user(username='testuser2', password='12345')
        self.author2 = Author.objects.create(user=self.u2, host="http://testserver", displayName="Test User 2",
                              github="github/test2.com", profileImage="profile/test2.com")
        self.friend_request = FriendRequest.objects.create(actor=self.author2, object=self.author)
        self.inbox.friend_requests.add(self.friend_request)
        self.post = Post.objects.create(title="Test Post 1", source="http://testserver", origin="http://testserver",
                                   description="Test Post 1 Description", contentType="text/plain",
                                   content="Test Post 1 Content", author=self.author)
        self.inbox.posts.add(self.post)

    def test_inbox_view(self):
        request = self.factory.get('/inbox/' + str(self.author.id))
        response = InboxView.as_view()(request, author_id=str(self.author.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "inbox")
        self.assertEqual(response.data["author"], "http://testserver/authors/" + str(self.author.id))

        # Confirm that the post is in the inbox
        self.assertEqual(response.data["items"][0][0]["type"], "post")
        self.assertEqual(response.data["items"][0][0]["title"], "Test Post 1")
        self.assertEqual(response.data["items"][0][0]["source"], "http://testserver")
        self.assertEqual(response.data["items"][0][0]["origin"], "http://testserver")
        self.assertEqual(response.data["items"][0][0]["description"], "Test Post 1 Description")
        self.assertEqual(response.data["items"][0][0]["contentType"], "text/plain")
        self.assertEqual(response.data["items"][0][0]["content"], "Test Post 1 Content")
        self.assertEqual(response.data["items"][0][0]["author"]["id"], str(self.author.id))
        self.assertEqual(response.data["items"][0][0]["author"]["host"], "http://testserver")
        self.assertEqual(response.data["items"][0][0]["author"]["displayName"], "Test User 1")
        self.assertEqual(response.data["items"][0][0]["author"]["url"], "http://testserver/authors/" + str(self.author.id))
        self.assertEqual(response.data["items"][0][0]["author"]["github"], "github/test1.com")
        self.assertEqual(response.data["items"][0][0]["author"]["profileImage"], "profile/test1.com")

        # Confirm that the friend request is in the inbox
        self.assertEqual(response.data["items"][0][1]["type"], "Follow")
        self.assertEqual(response.data["items"][0][1]["actor"]["id"], str(self.author2.id))
        self.assertEqual(response.data["items"][0][1]["actor"]["host"], "http://testserver")
        self.assertEqual(response.data["items"][0][1]["actor"]["displayName"], "Test User 2")
        self.assertEqual(response.data["items"][0][1]["actor"]["url"], "http://testserver/authors/" + str(self.author2.id))
        self.assertEqual(response.data["items"][0][1]["actor"]["github"], "github/test2.com")
        self.assertEqual(response.data["items"][0][1]["actor"]["profileImage"], "profile/test2.com")
        self.assertEqual(response.data["items"][0][1]["object"]["id"], str(self.author.id))
        self.assertEqual(response.data["items"][0][1]["object"]["host"], "http://testserver")
        self.assertEqual(response.data["items"][0][1]["object"]["displayName"], "Test User 1")
        self.assertEqual(response.data["items"][0][1]["object"]["url"], "http://testserver/authors/" + str(self.author.id))
        self.assertEqual(response.data["items"][0][1]["object"]["github"], "github/test1.com")
        self.assertEqual(response.data["items"][0][1]["object"]["profileImage"], "profile/test1.com")
        
    
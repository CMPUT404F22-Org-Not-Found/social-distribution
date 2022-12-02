"""Contains tests for the node app."""

from unittest import mock

from django.test import TestCase

from django.contrib.auth.models import User
from author.models import Author
from author.serializers import AuthorSerializer
from post.models import Post
from post.serializers import PostSerializer
from followers.models import FriendRequest
from followers.serializers import FriendRequestSerializer
from like.models import Like
from like.serializers import LikeSerializer
from inbox.models import Inbox
from node.models import Node
from node.node_connections import send_post_to_inboxes, send_friend_request_to_global_inbox, send_like_to_global_inbox


class NodeConnectionsTestCase(TestCase):
    """Tests for the node_connections module."""

    def setUp(self):
        """Set up the test case."""
        self.user1 = User.objects.create_user(username="test", password="test")
        self.author1 = Author.objects.create(user=self.user1, host="http://127.0.0.1/", displayName="Test User 1",
                              github="github/test1.com", profileImage="profile/test1.com")
        self.inbox = Inbox.objects.create(author=self.author1)

        self.user2 = User.objects.create_user(username="test2", password="test2")
        self.author2 = Author.objects.create(user=self.user2, host="http://127.0.0.1/", displayName="Test User 2",
                                github="github/test2.com", profileImage="profile/test2.com")
        self.inbox2 = Inbox.objects.create(author=self.author2)

        # Author 2 is a follower of author 1
        self.author1.followers.add(self.author2)

    def test_send_post_to_local_inbox(self):
        """Test sending a post to a local inbox."""
        post = Post.objects.create(title="Test Post", source="http://127.0.0.1/", origin="http://127.0.0.1/",
                                   description="Test Description", contentType="text/plain", content="Test Content",
                                   author=self.author1, visibility="PUBLIC", unlisted=False)

        self.assertEqual(self.inbox.posts.count(), 0)
        self.assertEqual(self.inbox2.posts.count(), 0)

        send_post_to_inboxes(post, self.author1)

        self.assertEqual(self.inbox.posts.count(), 1)
        self.assertEqual(self.inbox2.posts.count(), 1)

        # Confirm that the post is the same
        self.assertEqual(self.inbox.posts.first().title, post.title)
        self.assertEqual(self.inbox2.posts.first().title, post.title)
    
    def test_send_post_to_local_inbox_only_followers(self):
        """Test sending a post to a local inbox only to followers. Only author 2 should get the post."""
        post = Post.objects.create(title="Test Post", source="http://127.0.0.1/", origin="http://127.0.0.1/",
                                   description="Test Description", contentType="text/plain", content="Test Content",
                                   author=self.author1, visibility="PUBLIC", unlisted=False)

        self.assertEqual(self.inbox.posts.count(), 0)
        self.assertEqual(self.inbox2.posts.count(), 0)

        send_post_to_inboxes(post, self.author1, only_to_followers=True)

        self.assertEqual(self.inbox.posts.count(), 0)
        self.assertEqual(self.inbox2.posts.count(), 1)

        # Confirm that the post is the same
        self.assertEqual(self.inbox2.posts.first().title, post.title)

    def test_send_post_to_global_inbox(self):
        """Test sending a post to the global inbox."""
        post = Post.objects.create(title="Test Post", source="http://127.0.0.1/", origin="http://127.0.0.1/",
                                   description="Test Description", contentType="text/plain", content="Test Content",
                                   author=self.author1, visibility="PUBLIC", unlisted=False)

        # Make a global author
        node = Node.objects.create(host="http://testserver.com/", username="test", password="test")
        global_author = Author.objects.create(host="http://testserver.com/", displayName="Test User 3",
                                github="github/test3.com", profileImage="profile/test3.com")
        self.author1.followers.add(global_author)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        with mock.patch('node.node_connections.requests.post', return_value=mock_response) as mock_requests_post:
            send_post_to_inboxes(post, self.author1)

            # Check that the post was sent to the global inbox
            post_data = PostSerializer(post).data
            post_data.pop("commentsSrc")
            mock_requests_post.assert_called_once_with(
                f"{global_author.url}/inbox/",
                json=post_data, auth=("test", "test")
            )

    def test_send_friend_request_to_global_inbox(self):
        """Test sending a friend request to the global inbox."""
        # Make a global author
        node = Node.objects.create(host="http://testserver.com/", username="test", password="test")
        global_author = Author.objects.create(host="http://testserver.com/", displayName="Test User 3",
                                github="", profileImage="")
        # We create a friend request from author 1 to the global author
        friend_request = FriendRequest.objects.create(
            actor=self.author1, object=global_author, summary="Author 1 wants to follow with Author 3"
        )

        mock_response = mock.Mock()
        mock_response.status_code = 200
        with mock.patch('node.node_connections.requests.post', return_value=mock_response) as mock_requests_post:
            send_friend_request_to_global_inbox(friend_request, global_author)

            # Check that the friend request was sent to the global inbox
            friend_request_data = FriendRequestSerializer(friend_request).data
            mock_requests_post.assert_called_once_with(
                f"{global_author.url}/inbox/",
                json=friend_request_data, auth=("test", "test")
            )

    def test_send_like_to_global_inbox(self):
        """Test sending a like to the global inbox."""
        # Make a global author
        node = Node.objects.create(host="http://testserver.com/", username="test", password="test")
        global_author = Author.objects.create(host="http://testserver.com/", displayName="Test User 3",
                                github="", profileImage="")
        # We create a like from author 1 to a post from the global author
        post = Post.objects.create(title="Test Post", source="http://testserver.com/", origin="http://testserver.com/",
                                      description="Test Description", contentType="text/plain", content="Test Content",
                                        author=global_author, visibility="PUBLIC", unlisted=False)
        like = Like.objects.create(author=self.author1, object=post.url, summary="Author 1 likes a post from Author 3")

        mock_response = mock.Mock()
        mock_response.status_code = 200
        with mock.patch('node.node_connections.requests.post', return_value=mock_response) as mock_requests_post:
            send_like_to_global_inbox(like, global_author)

            # Check that the like was sent to the global inbox
            like_data = LikeSerializer(like).data
            mock_requests_post.assert_called_once_with(
                f"{global_author.url}/inbox/",
                json=like_data, auth=("test", "test")
            )
"""Contains tests for the Like app."""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase, APIRequestFactory

from author.models import Author
from post.models import Post
from .models import Like
from .views import LikeView


class LikeModelTestCase(TestCase):
    """Tests for the Like model."""

    def setUp(self):
        """Set up the test case."""
        self.user = User.objects.create_user(username="test", password="test")
        self.author = Author.objects.create(user=self.user, displayName="Test", host="http://test.com")

        self.like = Like.objects.create(author=self.author, object="http://test.com/1", summary="Test likes test post.")

    def test_like_model(self):
        """Test the Like model."""
        self.assertEqual(self.like.type, "Like")
        self.assertEqual(self.like.author, self.author)
        self.assertEqual(self.like.object, "http://test.com/1")
        self.assertEqual(self.like.summary, "Test likes test post.")

    def test_like_model_str(self):
        """Test the string representation of the Like model."""
        self.assertEqual(str(self.like), f"{self.author.displayName} liked {self.like.object}")

    def test_like_model_unique(self):
        """Test that the Like model is unique."""
        with self.assertRaises(Exception):
            Like.objects.create(author=self.author, object="http://test.com/1", summary="Test")

    def test_like_model_delete(self):
        """Test that the Like model is deleted when the author is deleted."""
        self.author.delete()
        self.assertEqual(Like.objects.count(), 0)


class LikeViewTestCase(APITestCase):
    """Tests for the Like view."""

    def setUp(self):
        """Set up the test case."""
        self.user = User.objects.create_user(username="test", password="test")
        self.author = Author.objects.create(user=self.user, displayName="Test", host="http://test.com")
        self.post = Post.objects.create(title="Test", source="http://test.com/1", origin="http://test.com/1", 
                                        description="Test post", contentType="text/plain",
                                        content="Test post", author=self.author,
                                        url=f"http://test.com/authors/{self.author.id}/1", visibility="PUBLIC")
        self.client.force_authenticate(user=self.user)

        self.like = Like.objects.create(author=self.author, object=self.post.url, summary="Test likes test post.")

    def test_like_view_get(self):
        """Test the GET method of the Like view."""
        response = self.client.get(f"/authors/{self.author.author_id}/posts/{self.post.post_id}/likes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "likes")
        self.assertEqual(response.data["items"][0]["type"], "Like")
        self.assertEqual(response.data["items"][0]["author"]["id"], str(self.author.id))
        self.assertEqual(response.data["items"][0]["object"], self.post.url)
        self.assertEqual(response.data["items"][0]["summary"], "Test likes test post.")

    def test_like_view_get_comment(self):
        """Test the GET method of the Like view with a comment."""
        response = self.client.get(f"/authors/{self.author.author_id}/posts/{self.post.id}/comments/1/likes")
        self.assertEqual(response.status_code, 404)

    def test_like_view_get_no_author(self):
        """Test the GET method of the Like view with a non-existent author."""
        response = self.client.get(f"/authors/1/posts/{self.post.id}/likes")
        self.assertEqual(response.status_code, 404)

    def test_like_view_POST(self):
        """Send a POST to the Like view. This says author like the post, both are given in the url."""
        post2 = Post.objects.create(title="Test Post 2", source="http://test.com/2", origin="http://test.com/1", 
                                        description="Test post 2", contentType="text/plain",
                                        content="Test post", author=self.author,
                                        url=f"http://test.com/authors/{self.author.id}/2", visibility="PUBLIC")

        response = self.client.post(f"/authors/{self.author.author_id}/posts/{post2.post_id}/likes/")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["type"], "Like")
        self.assertEqual(response.data["detail"], f"{self.author.displayName} liked {post2.url}.")

        # Check that the like was created
        self.assertEqual(Like.objects.count(), 2)
        created_like = Like.objects.get(author=self.author, object=post2.url)
        self.assertIsNotNone(created_like)
        self.assertEqual(created_like.summary, f"{self.author.displayName} likes {post2.title}.")


class LikedViewTest(APITestCase):
    """Tests for the Liked view."""

    def setUp(self):
        """Set up the test case."""
        self.user = User.objects.create_user(username="test", password="test")
        self.author = Author.objects.create(user=self.user, displayName="Test", host="http://test.com")
        self.post = Post.objects.create(title="Test", source="http://test.com/1", origin="http://test.com/1", 
                                        description="Test post", contentType="text/plain",
                                        content="Test post", author=self.author,
                                        url=f"http://test.com/authors/{self.author.id}/1", visibility="PUBLIC")

        self.like = Like.objects.create(author=self.author, object=self.post.url, summary="Test likes test post.")

    def test_liked_view_get(self):
        """Test the GET method of the Liked view."""
        response = self.client.get(f"/authors/{self.author.author_id}/liked/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "liked")
        self.assertEqual(response.data["items"][0]["type"], "Like")
        self.assertEqual(response.data["items"][0]["author"]["id"], str(self.author.id))
        self.assertEqual(response.data["items"][0]["object"], self.post.url)
        self.assertEqual(response.data["items"][0]["summary"], "Test likes test post.")

    def test_liked_view_get_no_author(self):
        """Test the GET method of the Liked view with a non-existent author."""
        response = self.client.get(f"/authors/1/liked/")
        self.assertEqual(response.status_code, 404)



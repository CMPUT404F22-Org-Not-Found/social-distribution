"""Contains the tests for the Inbox app."""

from unittest import skip
import uuid

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase, APIRequestFactory, force_authenticate

from author.models import Author
from post.models import Post
from followers.models import FriendRequest
from inbox.models import Inbox
from inbox.views import InboxView
from like.models import Like


class InboxModelTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create_user(username='testuser1', password='12345')
        author = Author.objects.create(user=u1, host="http://testserver/", displayName="Test User 1",
                              github="github/test1.com", profileImage="profile/test1.com")
        Inbox.objects.create(author=author)

    def test_inbox_model(self):
        inbox = Inbox.objects.get(author__user__username='testuser1')
        self.assertEqual(inbox.type, "inbox")
        self.assertEqual(inbox.author.displayName, "Test User 1")
        self.assertEqual(inbox.author.github, "github/test1.com")
        self.assertEqual(inbox.author.profileImage, "profile/test1.com")
        self.assertEqual(inbox.author.host, "http://testserver/")
        self.assertEqual(inbox.author.url, "http://testserver/authors/" + str(inbox.author.author_id))

    def test_inbox_model_str(self):
        inbox = Inbox.objects.get(author__user__username='testuser1')
        self.assertEqual(str(inbox), "Inbox of Test User 1 - " + str(inbox.author.author_id))

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
        self.author = Author.objects.create(user=self.u1, host="http://testserver/", displayName="Test User 1",
                              github="github/test1.com", profileImage="profile/test1.com")
        self.inbox = Inbox.objects.create(author=self.author)
        self.client.force_authenticate(user=self.u1)
        self.u2 = User.objects.create_user(username='testuser2', password='12345')
        self.author2 = Author.objects.create(user=self.u2, host="http://testserver/", displayName="Test User 2",
                              github="github/test2.com", profileImage="profile/test2.com")
        self.inbox2 = Inbox.objects.create(author=self.author2)
        self.friend_request = FriendRequest.objects.create(actor=self.author2, object=self.author)
        self.inbox.friend_requests.add(self.friend_request)
        self.post = Post.objects.create(title="Test Post 1", source="http://testserver", origin="http://testserver",
                                   description="Test Post 1 Description", contentType="text/plain",
                                   content="Test Post 1 Content", author=self.author)
        self.inbox.posts.add(self.post)

    def test_inbox_view(self):
        request = self.factory.get('/inbox/' + str(self.author.author_id))
        force_authenticate(request, user=self.u1)
        response = InboxView.as_view()(request, author_id=str(self.author.author_id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "inbox")
        self.assertEqual(response.data["author"], "http://testserver/authors/" + str(self.author.author_id))

        # Confirm that the post is in the inbox
        self.assertEqual(response.data["items"][0]["type"], "post")
        self.assertEqual(response.data["items"][0]["title"], "Test Post 1")
        self.assertEqual(response.data["items"][0]["source"], "http://testserver" + "posts/" + str(self.post.post_id))
        self.assertEqual(response.data["items"][0]["origin"], "http://testserver" + "posts/" + str(self.post.post_id))
        self.assertEqual(response.data["items"][0]["description"], "Test Post 1 Description")
        self.assertEqual(response.data["items"][0]["contentType"], "text/plain")
        self.assertEqual(response.data["items"][0]["content"], "Test Post 1 Content")
        self.assertEqual(response.data["items"][0]["author"]["id"], str(self.author.id))
        self.assertEqual(response.data["items"][0]["author"]["host"], "http://testserver/")
        self.assertEqual(response.data["items"][0]["author"]["displayName"], "Test User 1")
        self.assertEqual(response.data["items"][0]["author"]["url"], "http://testserver/authors/" + str(self.author.author_id))
        self.assertEqual(response.data["items"][0]["author"]["github"], "github/test1.com")
        self.assertEqual(response.data["items"][0]["author"]["profileImage"], "profile/test1.com")

        # Confirm that the friend request is in the inbox
        self.assertEqual(response.data["items"][1]["type"], "Follow")
        self.assertEqual(response.data["items"][1]["actor"]["id"], str(self.author2.id))
        self.assertEqual(response.data["items"][1]["actor"]["host"], "http://testserver/")
        self.assertEqual(response.data["items"][1]["actor"]["displayName"], "Test User 2")
        self.assertEqual(response.data["items"][1]["actor"]["url"], "http://testserver/authors/" + str(self.author2.author_id))
        self.assertEqual(response.data["items"][1]["actor"]["github"], "github/test2.com")
        self.assertEqual(response.data["items"][1]["actor"]["profileImage"], "profile/test2.com")
        self.assertEqual(response.data["items"][1]["object"]["id"], str(self.author.id))
        self.assertEqual(response.data["items"][1]["object"]["host"], "http://testserver/")
        self.assertEqual(response.data["items"][1]["object"]["displayName"], "Test User 1")
        self.assertEqual(response.data["items"][1]["object"]["url"], "http://testserver/authors/" + str(self.author.author_id))
        self.assertEqual(response.data["items"][1]["object"]["github"], "github/test1.com")
        self.assertEqual(response.data["items"][1]["object"]["profileImage"], "profile/test1.com")
        
    def test_inbox_view_no_inbox(self):
        request = self.factory.get('/inbox/999')
        force_authenticate(request, user=self.u1)
        response = InboxView.as_view()(request, author_id=999)

        self.assertEqual(response.status_code, 404)

    def test_inbox_view_no_items(self):
        self.inbox.posts.clear()
        self.inbox.friend_requests.clear()
        request = self.factory.get('/inbox/' + str(self.author.author_id))
        force_authenticate(request, user=self.u1)
        response = InboxView.as_view()(request, author_id=str(self.author.author_id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "inbox")
        self.assertEqual(response.data["author"], "http://testserver/authors/" + str(self.author.author_id))
        self.assertEqual(len(response.data["items"]), 0)
    
    def test_inbox_view_no_author(self):
        request = self.factory.get('/inbox/999')
        force_authenticate(request, user=self.u1)
        response = InboxView.as_view()(request, author_id=999)

        self.assertEqual(response.status_code, 404)
    
    def test_inbox_POST_with_existing_post(self):
        """When we POST a post to the inbox, if the post is already present, add the post to the inbox,
        if the post is not present, create a new post and add it to the inbox.
        """
        data = {
            "type": "post",
            "id": self.post.id,
            "title": "Test Post 1",
            "source": "http://testserver",
            "origin": "http://testserver",
            "description": "Test Post 1 Description",
            "contentType": "text/plain",
            "content": "Test Post 1 Content",
            "author": {
                "id": str(self.author.id),
                "host": "http://testserver",
                "displayName": "Test User 1",
                "url": "http://testserver/authors/" + str(self.author.author_id),
                "github": "github/test1.com",
                "profileImage": "profile/test1.com"
            }
        }
        request = self.factory.post('/inbox/' + str(self.author.author_id), data, format='json')
        force_authenticate(request, user=self.u1)
        response = InboxView.as_view()(request, author_id=str(self.author.author_id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "post")
        self.assertEqual(response.data["detail"], f"Successfully sent the post to {self.author.displayName}'s inbox")

        # Check that the post is in the inbox
        self.assertEqual(self.inbox.posts.count(), 1)
        self.assertEqual(self.inbox.posts.first().title, "Test Post 1")
        self.assertEqual(self.inbox.posts.first().source, "http://testserver")
        self.assertEqual(self.inbox.posts.first().origin, "http://testserver")
        self.assertEqual(self.inbox.posts.first().description, "Test Post 1 Description")
        self.assertEqual(self.inbox.posts.first().contentType, "text/plain")
        self.assertEqual(self.inbox.posts.first().content, "Test Post 1 Content")
        self.assertEqual(str(self.inbox.posts.first().author.id), str(self.author.id))
        self.assertEqual(self.inbox.posts.first().author.host, "http://testserver/")
        self.assertEqual(self.inbox.posts.first().author.displayName, "Test User 1")
        self.assertEqual(self.inbox.posts.first().author.url, "http://testserver/authors/" + str(self.author.author_id))
        self.assertEqual(self.inbox.posts.first().author.github, "github/test1.com")
        self.assertEqual(self.inbox.posts.first().author.profileImage, "profile/test1.com")

    def test_inbox_POST_with_new_post(self):
        """When we POST a post to the inbox, if the post is already present, add the post to the inbox,
        if the post is not present, create a new post and add it to the inbox.
        """
        data = {
            "type": "post",
            "title": "Test Post 2",
            "source": "http://testserver",
            "origin": "http://testserver",
            "description": "Test Post 2 Description",
            "contentType": "text/plain",
            "content": "Test Post 2 Content",
            "commentsSrc": "needs to be deleted",   # we add this extra field that should be deleted by verify_post
            "author": {
                "id": str(self.author.id),
                "host": "http://testserver",
                "displayName": "Test User 1",
                "url": "http://testserver/authors/" + str(self.author.author_id),
                "github": "github/test1.com",
                "profileImage": "profile/test1.com"
            }
        }
        request = self.factory.post('/inbox/' + str(self.author.author_id), data, format='json')
        force_authenticate(request, user=self.u1)
        response = InboxView.as_view()(request, author_id=str(self.author.author_id))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["type"], "post")
        self.assertEqual(response.data["detail"], f"Successfully created a new post and sent to {self.author.displayName}'s inbox")

        # Check that the post is in the inbox
        self.assertEqual(self.inbox.posts.count(), 2)
        added_post = self.inbox.posts.filter(title="Test Post 2").first()
        self.assertEqual(added_post.title, "Test Post 2")
        self.assertEqual(added_post.source, "http://testserver")
        self.assertEqual(added_post.origin, "http://testserver")
        self.assertEqual(added_post.description, "Test Post 2 Description")
        self.assertEqual(added_post.contentType, "text/plain")
        self.assertEqual(added_post.content, "Test Post 2 Content")
        self.assertEqual(str(added_post.author.id), str(self.author.id))
        self.assertEqual(added_post.author.host, "http://testserver/")
        self.assertEqual(added_post.author.displayName, "Test User 1")
        self.assertEqual(added_post.author.url, "http://testserver/authors/" + str(self.author.author_id))
        self.assertEqual(added_post.author.github, "github/test1.com")

    def test_inbox_POST_with_new_post_new_author(self):
        """For posts coming from a remote server, we will create a new author if the author does not exist.
            And add the post to the inbox.
        """
        # Here a new author (Test User 3) is a remote author and is sending a post to the inbox of Test User 1
        new_author_uuid = uuid.uuid4()
        data = {
            "type": "post",
            "title": "Test Post 3",
            "source": "http://testserver",
            "origin": "http://testserver",
            "description": "Test Post 3 Description",
            "contentType": "text/plain",
            "content": "Test Post 3 Content",
            "author": {
                "id": f"http://testserver/authors/{new_author_uuid}",
                "host": "http://testserver/",
                "displayName": "Test User 3",
                "url": "http://testserver/authors/999",
                "github": "github/test3.com",
                "profileImage": "profile/test3.com",
                "uuid": str(new_author_uuid)    # we add this extra field that should be deleted by verify_author
            }
        }
        request = self.factory.post('/inbox/' + str(self.author.author_id), data, format='json')
        force_authenticate(request, user=self.u1)
        response = InboxView.as_view()(request, author_id=str(self.author.author_id))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["type"], "post")
        self.assertEqual(response.data["detail"], f"Successfully created a new post and sent to Test User 1's inbox")

        # Check that the post is in the inbox
        self.assertEqual(self.inbox.posts.count(), 2)
        added_post = self.inbox.posts.filter(title="Test Post 3").first()
        self.assertEqual(added_post.title, "Test Post 3")
        self.assertEqual(added_post.source, "http://testserver")
        self.assertEqual(added_post.origin, "http://testserver")
        self.assertEqual(added_post.description, "Test Post 3 Description")
        self.assertEqual(added_post.contentType, "text/plain")
        self.assertEqual(added_post.content, "Test Post 3 Content")
        self.assertEqual(str(added_post.author.author_id), str(new_author_uuid))
        self.assertEqual(added_post.author.host, "http://testserver/")
        self.assertEqual(added_post.author.displayName, "Test User 3")
        self.assertEqual(added_post.author.url, "http://testserver/authors/" + str(new_author_uuid))
        self.assertEqual(added_post.author.github, "github/test3.com")
        self.assertEqual(added_post.author.profileImage, "profile/test3.com")

        # Check that the new remote author is created
        self.assertEqual(Author.objects.count(), 3)
        new_author = Author.objects.filter(displayName="Test User 3").first()
        self.assertEqual(str(new_author.author_id), str(new_author_uuid))
 
    def test_inbox_POST_follow_request_with_existing_authors(self):
        """Create a friend request from author 1 to author 2."""
        data = {
            "type": "follow",
            "summary": "Test User 1 wants to follow Test User 2",
            "actor": {
                "id": str(self.author.author_id),
                "host": "http://testserver",
                "displayName": "Test User 1",
                "url": "http://testserver/authors/" + str(self.author.author_id),
                "github": "github/test1.com",
                "profileImage": "profile/test1.com"
            },
            "object": {
                "id": str(self.author2.author_id),
                "host": "http://testserver",
                "displayName": "Test User 2",
                "url": "http://testserver/authors/" + str(self.author2.author_id),
                "github": "github/test2.com",
                "profileImage": "profile/test2.com"
            }
        }
        request = self.factory.post('/inbox/' + str(self.author2.author_id), data, format='json')
        force_authenticate(request, user=self.u2)
        response = InboxView.as_view()(request, author_id=str(self.author2.author_id))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["type"], "follow")
        self.assertEqual(response.data["detail"], f"Successfully created a new follow request and sent to {self.author2.displayName}'s inbox")

        # Check that the friend request is in the inbox
        self.assertEqual(self.inbox2.friend_requests.count(), 1)
        added_friend_request = self.inbox2.friend_requests.filter(actor=self.author).first()
        self.assertEqual(str(added_friend_request.actor.id), str(self.author.id))
        self.assertEqual(added_friend_request.actor.displayName, "Test User 1")
        self.assertEqual(str(added_friend_request.object.id), str(self.author2.id))
        self.assertEqual(added_friend_request.object.displayName, "Test User 2")

    def test_inbox_POST_follow_request_with_new_author(self):
        """Create a friend request from a new author (the remote author) to author 2."""
        new_author_uuid = uuid.uuid4()
        data = {
            "type": "follow",
            "summary": "Test User 3 wants to follow Test User 2",
            "actor": {
                "id": f"http://testserver/authors/{new_author_uuid}",
                "host": "http://testserver",
                "displayName": "Test User 3",
                "url": "http://testserver/authors/" + str(new_author_uuid),
                "github": "github/test3.com",
                "profileImage": "profile/test3.com"
            },
            "object": {
                "id": str(self.author2.id),
                "host": "http://testserver",
                "displayName": "Test User 2",
                "url": "http://testserver/authors/" + str(self.author2.author_id),
                "github": "github/test2.com",
                "profileImage": "profile/test2.com"
            }
        }
        request = self.factory.post('/inbox/' + str(self.author2.author_id), data, format='json')
        force_authenticate(request, user=self.u2)
        response = InboxView.as_view()(request, author_id=str(self.author2.author_id))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["type"], "follow")
        self.assertEqual(response.data["detail"], f"Successfully created a new follow request and sent to {self.author2.displayName}'s inbox")

        # Check that the friend request is in the inbox
        self.assertEqual(self.inbox2.friend_requests.count(), 1)
        added_friend_request = self.inbox2.friend_requests.filter(actor__author_id=new_author_uuid).first()
        self.assertEqual(str(added_friend_request.actor.author_id), str(new_author_uuid))
        self.assertEqual(added_friend_request.actor.displayName, "Test User 3")
        self.assertEqual(str(added_friend_request.object.id), str(self.author2.id))
        self.assertEqual(added_friend_request.object.displayName, "Test User 2")

        # Check that the new remote author is created
        self.assertEqual(Author.objects.count(), 3)
        new_author = Author.objects.filter(displayName="Test User 3").first()
        self.assertEqual(str(new_author.author_id), str(new_author_uuid))

    def test_inbox_POST_follow_request_with_existing_authors_and_existing_friend_request(self):
        """Create a friend request from author 1 to author 2, but the friend request already exists."""
        # Create a friend request from author 1 to author 2
        self.inbox2.friend_requests.create(actor=self.author, object=self.author2)

        data = {
            "type": "follow",
            "summary": "Test User 1 wants to follow Test User 2",
            "actor": {
                "id": str(self.author.id),
                "host": "http://testserver",
                "displayName": "Test User 1",
                "url": "http://testserver/authors/" + str(self.author.author_id),
                "github": "github/test1.com",
                "profileImage": "profile/test1.com"
            },
            "object": {
                "id": str(self.author2.id),
                "host": "http://testserver",
                "displayName": "Test User 2",
                "url": "http://testserver/authors/" + str(self.author2.author_id),
                "github": "github/test2.com",
                "profileImage": "profile/test2.com"
            }
        }
        request = self.factory.post('/inbox/' + str(self.author2.author_id), data, format='json')
        force_authenticate(request, user=self.u2)
        response = InboxView.as_view()(request, author_id=str(self.author2.author_id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "follow")
        self.assertEqual(response.data["detail"], f"Successfully sent the follow request to {self.author2.displayName}'s inbox")

        # Check that the friend request is in the inbox
        self.assertEqual(self.inbox2.friend_requests.count(), 1)
        added_friend_request = self.inbox2.friend_requests.filter(actor=self.author).first()
        self.assertEqual(str(added_friend_request.actor.id), str(self.author.id))
        self.assertEqual(added_friend_request.actor.displayName, "Test User 1")
        self.assertEqual(str(added_friend_request.object.id), str(self.author2.id))
        self.assertEqual(added_friend_request.object.displayName, "Test User 2")

    def test_inbox_POST_like_request_with_existing_authors(self):
        """Send a like object of author 1 liking a post from author 2 to author 2's inbox."""
        # Create a post from author 2
        post = Post.objects.create(
            title="Test Post 1",
            source="http://testserver/posts/" + str(self.post.id),
            origin="http://testserver/posts/" + str(self.post.id),
            description="Test Post 1 Description",
            contentType="text/plain",
            content="Test Post 1 Content",
            author=self.author2,
            visibility="PUBLIC",
            unlisted=False
        )
        post.url = f"http://testserver/authors/{self.author2.author_id}/{post.post_id}"
        post.save()

        data = {
            "type": "like",
            "summary": "Test User 1 likes Test Post 1",
            "author": {
                "id": str(self.author.id),
                "host": "http://testserver",
                "displayName": "Test User 1",
                "url": "http://testserver/authors/" + str(self.author.author_id),
                "github": "github/test1.com",
                "profileImage": "profile/test1.com"
            },
            "object": post.url
        }
        request = self.factory.post('/inbox/' + str(self.author2.author_id), data, format='json')
        force_authenticate(request, user=self.u2)
        response = InboxView.as_view()(request, author_id=str(self.author2.author_id))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["type"], "like")
        self.assertEqual(response.data["detail"], f"Successfully created a new like and sent to {self.author2.displayName}'s inbox")

        # Check that the like request is in the inbox
        self.assertEqual(self.inbox2.likes.count(), 1)
        added_like_request = self.inbox2.likes.filter(author=self.author).first()
        self.assertEqual(str(added_like_request.author.id), str(self.author.id))
        self.assertEqual(added_like_request.object, post.url)
        self.assertEqual(added_like_request.summary, "Test User 1 likes Test Post 1")
    
    def test_inbox_POST_like_request_with_existing_authors_and_existing_like_request(self):
        """Send a like object of author 1 liking a post from author 2 to author 2's inbox, but the like request already exists."""
        # Create a post from author 2
        post = Post.objects.create(
            title="Test Post 1",
            source="http://testserver/posts/" + str(self.post.post_id),
            origin="http://testserver/posts/" + str(self.post.post_id),
            description="Test Post 1 Description",
            contentType="text/plain",
            content="Test Post 1 Content",
            author=self.author2,
            visibility="PUBLIC",
            unlisted=False
        )
        post.url = f"http://testserver/authors/{self.author2.author_id}/{post.post_id}"
        post.save()

        # Create a like request from author 1 to author 2's post
        self.inbox2.likes.create(author=self.author, object=post.url, summary="Test User 1 likes Test Post 1")

        data = {
            "type": "like",
            "summary": "Test User 1 likes Test Post 1",
            "author": {
                "id": str(self.author.id),
                "host": "http://testserver",
                "displayName": "Test User 1",
                "url": "http://testserver/authors/" + str(self.author.id),
                "github": "github/test1.com",
                "profileImage": "profile/test1.com"
            },
            "object": post.url
        }
        request = self.factory.post('/inbox/' + str(self.author2.author_id), data, format='json')
        force_authenticate(request, user=self.u2)
        response = InboxView.as_view()(request, author_id=str(self.author2.author_id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "like")
        self.assertEqual(response.data["detail"], f"Successfully sent the like to {self.author2.displayName}'s inbox")

        # Check that the like request is in the inbox
        self.assertEqual(self.inbox2.likes.count(), 1)
        added_like_request = self.inbox2.likes.filter(author=self.author).first()
        self.assertEqual(str(added_like_request.author.id), str(self.author.id))
        self.assertEqual(added_like_request.object, post.url)
        self.assertEqual(added_like_request.summary, "Test User 1 likes Test Post 1")

    def test_inbox_POST_like_request_with_new_author(self):
        """Send a like object of a remote author liking a post from author 2 to author 2's inbox."""
        # Create a post from author 2
        post = Post.objects.create(
            title="Test Post 1",
            source="http://testserver/posts/" + str(self.post.post_id),
            origin="http://testserver/posts/" + str(self.post.post_id),
            description="Test Post 1 Description",
            contentType="text/plain",
            content="Test Post 1 Content",
            author=self.author2,
            visibility="PUBLIC",
            unlisted=False
        )
        post.url = f"http://testserver/authors/{self.author2.author_id}/{post.post_id}"
        post.save()

        new_author_uuid = uuid.uuid4()
        data = {
            "type": "like",
            "summary": "Remote author 1 likes Test Post 1",
            "author": {
                "id": f"http://testserver/authors/{new_author_uuid}",
                "host": "http://testserver",
                "displayName": "Test User 3",
                "url": "http://testserver/authors/" + str(new_author_uuid),
                "github": "github/test3.com",
                "profileImage": "profile/test3.com",
                "uuid": str(new_author_uuid),   # we add this extra field, which needs to be deleted by verify_author
            },
            "object": post.url
        }

        request = self.factory.post('/inbox/' + str(self.author2.author_id), data, format='json')
        force_authenticate(request, user=self.u2)
        response = InboxView.as_view()(request, author_id=str(self.author2.author_id))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["type"], "like")
        self.assertEqual(response.data["detail"], f"Successfully created a new like and sent to {self.author2.displayName}'s inbox")

        # Check that the like request is in the inbox
        self.assertEqual(self.inbox2.likes.count(), 1)
        added_like_request = self.inbox2.likes.filter(author__author_id=new_author_uuid).first()
        self.assertEqual(str(added_like_request.author.author_id), str(new_author_uuid))
        self.assertEqual(added_like_request.object, post.url)
        self.assertEqual(added_like_request.summary, "Remote author 1 likes Test Post 1")

        # Check that the new remote author is created
        self.assertEqual(Author.objects.count(), 3)
        new_author = Author.objects.filter(displayName="Test User 3").first()
        self.assertEqual(str(new_author.author_id), str(new_author_uuid))

    def test_inbox_delete(self):
        """Clear an inbox."""
        self.assertEqual(self.inbox.posts.count(), 1)
        self.assertEqual(self.inbox.friend_requests.count(), 1)

        request = self.factory.delete('/inbox/' + str(self.author.author_id))
        force_authenticate(request, user=self.u1)
        response = InboxView.as_view()(request, author_id=str(self.author.author_id))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.inbox.posts.count(), 0)
        self.assertEqual(self.inbox.friend_requests.count(), 0)

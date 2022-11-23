from comment.views import CommentDetail
from author.serializers import AuthorSerializer
from django.test import TestCase
from author.models import Author
from post.models import Post
from .models import Comment
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient, APIRequestFactory


# Create your tests here.
class CommentModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username = "test", password = "test")
        self.author1 = Author.objects.create(user = self.user1, displayName = "Test", host = "http://127.0.0.1:8000/")
        self.user2 = User.objects.create_user(username = "test2", password = "test")
        self.author2 = Author.objects.create(user = self.user2, displayName = "Test1", host = "http://127.0.0.1:8000/")
        self.post = Post.objects.create(
            title="Test Title",
            source = "http://127.0.0.1:8000/",
            origin = "http://127.0.0.1:8000/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test content",
            author = self.author1,
        )

        self.comment = Comment.objects.create(post = self.post, author = self.author2, comment = "test")

    def test_comment(self):
        comment = Comment.objects.get(id = self.comment.id)
        comment_text = comment.comment
        self.assertEqual(comment_text,self.comment.comment)

    def test_author(self):
        comment = Comment.objects.get(id = self.comment.id)
        author = comment.author
        self.assertEqual(author,self.author2)
    
    def test_post(self):
        comment = Comment.objects.get(id = self.comment.id)
        post = comment.post
        self.assertEqual(post,self.post)
    

class CommentDetailTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username = "test", password = "test")
        self.author1 = Author.objects.create(user = self.user1, displayName = "Test", host = "http://127.0.0.1:8000/")
        self.user2 = User.objects.create_user(username = "test2", password = "test")
        self.author2 = Author.objects.create(user = self.user2, displayName = "Test1", host = "http://127.0.0.1:8000/")
        self.client = APIClient()
        self.factory = APIRequestFactory()
        
        self.post = Post.objects.create(
            title="Test Title",
            source = "http://127.0.0.1:8000/",
            origin = "http://127.0.0.1:8000/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test content",
            author = self.author1,
        )

        self.comment1 = Comment.objects.create(post = self.post, author = self.author2, comment = "test")
        self.comment2 = Comment.objects.create(post = self.post, author = self.author1, comment = "test2")

    def test_comment_get(self):
        req = self.factory.get('/authors/{}/posts{}/comments/'.format(self.author1.author_id,self.post.post_id), format='json')        
        res = CommentDetail.as_view()(req,pk = self.author1.author_id, post_id = self.post.post_id)
        self.assertEqual(res.status_code,200)
        self.assertEqual(2,len(res.data["comments"]))

    def test_comment_post(self):
        self.assertEqual(2,len(self.post.post_comment.all()))
        data = {

            "type": "comment", 
            "comment": "Test comment", 
            "author": AuthorSerializer(self.author2).data,
            "contentType": "text/plain"
        }

        res = self.client.post('/authors/{}/posts/{}/comments/'.format(self.author1.author_id,self.post.post_id), data = data, format = 'json')
        self.assertEqual(res.status_code,201)
        self.assertEqual(3,len(self.post.post_comment.all()))
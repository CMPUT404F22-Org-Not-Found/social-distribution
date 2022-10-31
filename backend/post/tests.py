from uuid import uuid4
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from post.models import Post
from django.contrib.auth.models import User
from author.models import Author
from .views import PostDetail, PostList, PublicView

# Create your tests here.

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username = "test", password = "test")
        self.author = Author.objects.create(user = self.user, displayName = "Test", host = "http://127.0.0.1:8000/")

        self.post = Post.objects.create(
            title="Test Title",
            source = "http://127.0.0.1:8000/",
            origin = "http://127.0.0.1:8000/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test content",
            author = self.author,
        )

    def test_title(self):
        post = Post.objects.get(id = self.post.id)
        title = post.title
        self.assertEqual(title,"Test Title")
    
    def test_author(self):
        author = Author.objects.get(id = self.author.id)
        post = Post.objects.get(id = self.post.id)
        post_author = post.author
        self.assertEqual(author,post_author)

    def test_posted(self):
        author = Author.objects.get(id = self.author.id)
        post = Post.objects.get(id = self.post.id)
        self.assertEqual(post,author.post_author.get(id = self.post.id))

class PostDetailTest(APITestCase): 

    def setUp(self):
        self.user = User.objects.create_user(username = "test", password = "test")
        self.author = Author.objects.create(user = self.user, displayName = "Test", host = "http://127.0.0.1:8000/") 
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
    
            title="Test Title",
            source = "http://127.0.0.1:8000/",
            origin = "http://127.0.0.1:8000/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test content",
            author = self.author,
        )

    def author_404(self):
        uuid = uuid4()
        req = self.factory.get('/authors/{}/posts/{}/'.format(uuid,self.post.id),format = 'json')
        res = PostDetail.as_view()(req, pk = uuid, post_id = self.post.id )
        self.assertEqual(res.status_code,404)

    def post_404(self):
        uuid = uuid4()
        req = self.factory.get('/authors/{}/posts/{}/'.format(self.author.id,uuid),format = 'json')
        res = PostDetail.as_view()(req, pk = self.author.id, post_id = uuid )
        self.assertEqual(res.status_code,404)

    def valid_post(self):
        req = self.factory.get('/authors/{}/posts/{}/'.format(self.author.id,self.post.id),format = 'json')
        res = PostDetail.as_view()(req, pk = self.author.id, post_id = self.post.id)
        self.assertEqual(res.data["id"],self.post.id)
    

    def test_post_put(self):
        self.assertEqual(1, len(self.author.post_author.all()))

        data = {
            "type": "post", 
            "title": "Second post", 
            "description": "This is the second post", 
            "contentType": "text/plain",
            "content": "This is the second post content", 
            "categories": ["web", "tutorial"], 
            "visibility":"PUBLIC", 
        }

        res = self.client.put('/authors/{}/posts/{}/'.format(self.author.id,self.post.id), data = data, format = 'json')
        self.assertEqual(res.status_code,201)
        post = Post.objects.get(id = self.post.id)
        post_title = post.title
        self.assertEqual(post_title, "Second post")
        self.assertEqual(1, len(self.author.post_author.all()))

    def test_post_delete(self):
        self.assertEqual(1, len(self.author.post_author.all()))
        self.client.delete('/authors/{}/posts/{}/'.format(self.author.id,self.post.id))
        self.assertEqual(0, len(self.author.post_author.all()))


class PublicViewTest(APITestCase):

    def setUp(self):
        
        self.user1 = User.objects.create_user(username = "test", password = "test")
        self.user2 = User.objects.create_user(username = "test1", password = "test")
        self.author1 = Author.objects.create(user = self.user1, displayName = "Test", host = "http://127.0.0.1:8000/")
        self.author2 = Author.objects.create(user = self.user2, displayName = "Test1", host = "http://127.0.0.1:8000/") 
        self.client = APIClient()
        self.factory = APIRequestFactory()
        

        self.post1 = Post.objects.create(
           
            title="Test Title",
            source = "http://127.0.0.1:8000/",
            origin = "http://127.0.0.1:8000/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test content",
            author = self.author1,
        )

        self.post2 = Post.objects.create(
           
            title="Test Title2",
            source = "http://127.0.0.1:8000/",
            origin = "http://127.0.0.1:8000/",
            description = "Test Post2",
            contentType = "text/plain",
            content = "test content",
            author = self.author2,
        )

    def test_public_get(self):
        req = self.factory.get('/public', format='json')        
        res = PublicView.as_view()(req)
        self.assertEqual(res.status_code,200)
        self.assertEqual(2,len(res.data["items"]))

class PostListViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username = "test", password = "test")
        self.author = Author.objects.create(user = self.user, displayName = "Test", host = "http://127.0.0.1:8000/") 
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.client.force_authenticate(user=self.user)

        self.post1 = Post.objects.create(
    
            title="Test Title",
            source = "http://127.0.0.1:8000/",
            origin = "http://127.0.0.1:8000/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test content",
            author = self.author,
        )

        self.post2 = Post.objects.create(
    
            title="Test Title 1",
            source = "http://127.0.0.1:8000/",
            origin = "http://127.0.0.1:8000/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test content",
            author = self.author,
        )

    def test_post_get(self):
        req = self.factory.get('/authors/{}/posts'.format(self.author.id), format='json')        
        res = PostList.as_view()(req, pk = self.author.id)
        self.assertEqual(res.status_code,200)
        self.assertEqual(2,len(res.data["items"]))


    def test_post_post(self):
        self.assertEqual(2, len(self.author.post_author.all()))
        data = {
            "type": "post", 
            "title": "First post", 
            "description": "This is the first post", 
            "contentType": "text/plain",
            "content": "This is the first post content", 
            "categories": ["web", "tutorial"], 
            "visibility":"PUBLIC"
        }

        res = self.client.post('/authors/{}/posts/'.format(self.author.id), data = data)
        self.assertEqual(res.status_code,201)
        self.assertEqual(3, len(self.author.post_author.all()))
        
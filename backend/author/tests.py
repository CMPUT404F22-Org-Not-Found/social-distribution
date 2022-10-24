"""Contains test cases for the author app."""

from re import S
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase, APIRequestFactory

from .models import Author
from .views import AuthorDetail, AuthorList


class AuthorModelTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create_user(username='testuser1', password='12345')
        Author.objects.create(user=u1, host="http://testserver", displayName="Test User 1",
                              github="github/test1.com", profileImage="profile/test1.com")

    def test_author_model(self):
        author = Author.objects.get(user__username='testuser1')
        self.assertEqual(author.displayName, "Test User 1")
        self.assertEqual(author.github, "github/test1.com")
        self.assertEqual(author.profileImage, "profile/test1.com")
        self.assertEqual(author.host, "http://testserver")
        self.assertEqual(author.url, "http://testserver/authors/" + str(author.id))

    def test_author_model_str(self):
        author = Author.objects.get(user__username='testuser1')
        self.assertEqual(str(author), "Test User 1 - " + str(author.id))
    
    def test_author_model_compute_url(self):
        author = Author.objects.get(user__username='testuser1')
        self.assertEqual(author.compute_url(), "http://testserver/authors/" + str(author.id))
    
    def test_author_model_save(self):
        author = Author.objects.get(user__username='testuser1')
        author.save()
        self.assertEqual(author.url, "http://testserver/authors/" + str(author.id))
    
    def test_author_model_followers(self):
        author = Author.objects.get(user__username='testuser1')
        self.assertEqual(author.followers.count(), 0)
        u2 = User.objects.create_user(username='testuser2', password='12345')
        author2 = Author.objects.create(user=u2, host="http://testserver", displayName="Test User 2",
                              github="github/test2.com", profileImage="profile/test2.com")
        author.followers.add(author2)
        self.assertEqual(author.followers.count(), 1)
        self.assertEqual(author.followers.first(), author2)
        self.assertEqual(author2.following.count(), 1)
        self.assertEqual(author2.following.first(), author)


class AuthorListViewTest(APITestCase):
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

    def test_author_list_view(self):
        request = self.factory.get('/authors', format='json')
        response = AuthorList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["type"], "author")
        self.assertEqual(response.data[0]["id"], str(self.author.id))
        self.assertEqual(response.data[0]["host"], "http://testserver")
        self.assertEqual(response.data[0]["url"], "http://testserver/authors/" + str(self.author.id))
        self.assertEqual(response.data[0]["displayName"], "Test User 1")
        self.assertEqual(response.data[0]["github"], "github/test1.com")
        self.assertEqual(response.data[0]["profileImage"], "profile/test1.com")
    
        # Confirm author 2
        self.assertEqual(response.data[1]["type"], "author")
        self.assertEqual(response.data[1]["id"], str(self.author2.id))
        self.assertEqual(response.data[1]["host"], "http://testserver")
        self.assertEqual(response.data[1]["url"], "http://testserver/authors/" + str(self.author2.id))
        self.assertEqual(response.data[1]["displayName"], "Test User 2")
        self.assertEqual(response.data[1]["github"], "github/test2.com")
        self.assertEqual(response.data[1]["profileImage"], "profile/test2.com")
    
    def test_author_list_pagination(self):
        # Get page 2 with page size 1, it should return the second authors

        request = self.factory.get('/authors?page=2&size=1', format='json')
        response = AuthorList.as_view()(request)
        self.assertEqual(response.status_code, 200)

        # Confirm author 2
        self.assertEqual(response.data[0]["type"], "author")
        self.assertEqual(response.data[0]["id"], str(self.author2.id))
        self.assertEqual(response.data[0]["host"], "http://testserver")
        self.assertEqual(response.data[0]["url"], "http://testserver/authors/" + str(self.author2.id))
        self.assertEqual(response.data[0]["displayName"], "Test User 2")
        self.assertEqual(response.data[0]["github"], "github/test2.com")
        self.assertEqual(response.data[0]["profileImage"], "profile/test2.com")


class AuthorDetailViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser1', password='12345')
        self.author = Author.objects.create(user=self.user, host="http://testserver", displayName="Test User 1",
                              github="github/test1.com", profileImage="profile/test1.com")
        self.client.force_authenticate(user=self.user)

    def test_author_detail_view_get(self):
        request = self.factory.get('/authors/' + str(self.author.id), format='json')
        response = AuthorDetail.as_view()(request, pk=self.author.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["type"], "author")
        self.assertEqual(response.data["id"], str(self.author.id))
        self.assertEqual(response.data["host"], "http://testserver")
        self.assertEqual(response.data["url"], "http://testserver/authors/" + str(self.author.id))
        self.assertEqual(response.data["displayName"], "Test User 1")
        self.assertEqual(response.data["github"], "github/test1.com")
        self.assertEqual(response.data["profileImage"], "profile/test1.com")

    def test_author_detail_view_not_found(self):
        request = self.factory.get('/authors/100', format='json')
        response = AuthorDetail.as_view()(request, pk=100)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Not found.")
    
    def test_author_detail_view_post(self):
        data = {"type": "author", "id": str(self.author.id), "host": "http://testserver",
                "url": "http://testserver/authors/" + str(self.author.id), "displayName": "Test User 11",}
        response = self.client.post('/authors/' + str(self.author.id), data=data)

        self.assertEqual(response.status_code, 200)
        
        # Confirm author
        self.assertEqual(response.data["type"], "author")
        self.assertEqual(response.data["id"], str(self.author.id))
        self.assertEqual(response.data["host"], "http://testserver")
        self.assertEqual(response.data["url"], "http://testserver/authors/" + str(self.author.id))
        self.assertEqual(response.data["displayName"], "Test User 11")
        self.assertEqual(response.data["github"], "github/test1.com")
        self.assertEqual(response.data["profileImage"], "profile/test1.com")

from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create an author first
        self.author = Author.objects.create(name='Test Author')
        
        # Create a test book
        self.book_data = {
            'title': 'Test Book',
            'author': self.author.id,
            'publication_year': 2020
        }
        self.book = Book.objects.create(
            title=self.book_data['title'],
            author=self.author,
            publication_year=self.book_data['publication_year']
        )

    def test_retrieve_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_single_book(self):
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, 200)

    def test_create_book(self):
        self.client.login(username='testuser', password='testpass')
        new_book = {
            'title': 'New Book',
            'author': self.author.id,
            'publication_year': 2021
        }
        response = self.client.post('/api/books/create/', new_book)
        self.assertEqual(response.status_code, 201)

    def test_update_book(self):
        self.client.login(username='testuser', password='testpass')
        updated_data = {
            'title': 'Updated Book',
            'author': self.author.id,
            'publication_year': 2022
        }
        response = self.client.put(f'/api/books/{self.book.id}/update/', updated_data)
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(f'/api/books/{self.book.id}/delete/')
        self.assertEqual(response.status_code, 204)

    def test_filter_books(self):
        response = self.client.get('/api/books/?author__name=Test Author')
        self.assertEqual(response.status_code, 200)

    def test_search_books(self):
        response = self.client.get('/api/books/?search=Test')
        self.assertEqual(response.status_code, 200)

    def test_ordering_books(self):
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, 200)

    def test_permissions_for_create(self):
        new_book = {
            'title': 'New Book',
            'author': self.author.id,
            'publication_year': 2021
        }
        response = self.client.post('/api/books/create/', new_book)
        self.assertEqual(response.status_code, 403)
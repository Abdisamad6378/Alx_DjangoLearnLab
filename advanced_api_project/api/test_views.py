from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book
from .serializers import BookSerializer

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create a test book
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2020
        }
        self.book = Book.objects.create(**self.book_data)

    def test_retrieve_books(self):
        """Test retrieving a list of books"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_single_book(self):
        """Test retrieving a single book"""
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, 200)

    def test_create_book(self):
        """Test the creation of a book"""
        self.client.login(username='testuser', password='testpass')
        new_book = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2021
        }
        response = self.client.post('/api/books/', new_book)
        self.assertEqual(response.status_code, 201)

    def test_update_book(self):
        """Test updating an existing book"""
        self.client.login(username='testuser', password='testpass')
        updated_data = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'publication_year': 2022
        }
        response = self.client.put(f'/api/books/{self.book.id}/', updated_data)
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        """Test deleting a book"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, 204)

    def test_filter_books(self):
        """Test filtering books by title, author, and publication year"""
        response = self.client.get('/api/books/?author=Test Author')
        self.assertEqual(response.status_code, 200)

    def test_search_books(self):
        """Test searching books by title or author"""
        response = self.client.get('/api/books/?search=Test')
        self.assertEqual(response.status_code, 200)

    def test_ordering_books(self):
        """Test ordering books by title or publication year"""
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, 200)

    def test_permissions_for_create(self):
        """Test that creating a book is restricted to authenticated users"""
        new_book = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2021
        }
        response = self.client.post('/api/books/', new_book)
        self.assertEqual(response.status_code, 403)  # Forbidden
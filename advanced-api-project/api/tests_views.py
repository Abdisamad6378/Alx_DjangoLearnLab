"""
Unit Tests for Book API
=======================
Task 3: Comprehensive test suite for Django REST Framework APIs.
Run tests with: python manage.py test api
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer
from datetime import datetime


class BookAPITestCase(APITestCase):
    """Test case for Book API endpoints covering CRUD, filtering, searching, ordering, and permissions."""

    def setUp(self):
        """Set up test data before each test method - creates fresh test database."""
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

        # Create test authors
        self.author1 = Author.objects.create(name='John Smith')
        self.author2 = Author.objects.create(name='Jane Doe')

        # Create test books
        self.book1 = Book.objects.create(
            title='Python Programming',
            publication_year=2021,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Django for Beginners',
            publication_year=2020,
            author=self.author2
        )

        # API client
        self.client = APIClient()

        # URLs - MUST MATCH urls.py EXACTLY
        self.books_list_url = '/api/books/'
        self.book_detail_url = lambda pk: f'/api/books/{pk}/'
        self.book_create_url = '/api/books/create/'
        self.book_update_url = lambda pk: f'/api/books/update/{pk}/'
        self.book_delete_url = lambda pk: f'/api/books/delete/{pk}/'

    # ======================================================================
    # CRUD OPERATIONS TESTS
    # ======================================================================

    def test_create_book(self):
        """Test creating a new book as authenticated user."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Test Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Test creating a book as unauthenticated user should be forbidden."""
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_invalid_data(self):
        """Test creating a book with invalid data (future year)."""
        self.client.force_authenticate(user=self.user)
        future_year = datetime.now().year + 10
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_books(self):
        """Test retrieving list of all books."""
        response = self.client.get(self.books_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_single_book(self):
        """Test retrieving a single book by ID."""
        response = self.client.get(self.book_detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_retrieve_nonexistent_book(self):
        """Test retrieving a book that doesn't exist."""
        response = self.client.get(self.book_detail_url(99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_book(self):
        """Test updating a book as authenticated user."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Python Book',
            'publication_year': 2023,
            'author': self.author2.id
        }
        response = self.client.put(self.book_update_url(self.book1.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Python Book')

    def test_update_book_unauthenticated(self):
        """Test updating a book as unauthenticated user should be forbidden."""
        data = {'title': 'Hacked Title'}
        response = self.client.put(self.book_update_url(self.book1.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_book(self):
        """Test partially updating a book with PATCH."""
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Partially Updated'}
        response = self.client.patch(self.book_update_url(self.book1.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated')

    def test_delete_book(self):
        """Test deleting a book as authenticated user."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.book_delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        """Test deleting a book as unauthenticated user should be forbidden."""
        response = self.client.delete(self.book_delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_nonexistent_book(self):
        """Test deleting a book that doesn't exist."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.book_delete_url(99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ======================================================================
    # FILTERING TESTS
    # ======================================================================

    def test_filter_books(self):
        """Test filtering books by author name."""
        response = self.client.get(self.books_list_url, {'author__name': 'John Smith'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author_name'], 'John Smith')

    def test_filter_books_by_year_range(self):
        """Test filtering books by publication year range."""
        response = self.client.get(self.books_list_url, {
            'publication_year__gte': 2020,
            'publication_year__lte': 2021
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ======================================================================
    # SEARCHING TESTS
    # ======================================================================

    def test_search_books(self):
        """Test searching books by title."""
        response = self.client.get(self.books_list_url, {'search': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_author(self):
        """Test searching books by author name."""
        response = self.client.get(self.books_list_url, {'search': 'Smith'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ======================================================================
    # ORDERING TESTS
    # ======================================================================

    def test_ordering_books(self):
        """Test ordering books by title."""
        response = self.client.get(self.books_list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_books_descending(self):
        """Test ordering books by publication year descending."""
        response = self.client.get(self.books_list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    # ======================================================================
    # PERMISSIONS TESTS
    # ======================================================================

    def test_permissions_for_create(self):
        """Test that creating a book requires authentication."""
        # Without authentication
        data = {
            'title': 'Permission Test',
            'publication_year': 2024,
            'author': self.author1.id
        }
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # With authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_access_unauthenticated(self):
        """Test that unauthenticated users can read books."""
        response = self.client.get(self.books_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.book_detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthorSerializerTestCase(TestCase):
    """Test cases for AuthorSerializer."""

    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2023,
            author=self.author
        )

    def test_author_serializer_with_books(self):
        """Test AuthorSerializer includes nested books."""
        serializer = AuthorSerializer(self.author)
        self.assertIn('books', serializer.data)
        self.assertEqual(len(serializer.data['books']), 1)
        self.assertIn('book_count', serializer.data)
        self.assertEqual(serializer.data['book_count'], 1)


# ======================================================================
# TEST DATABASE CONFIGURATION
# ======================================================================

"""
Test Database Configuration:
Django automatically creates a separate test database when running tests.
The database is configured in settings.py with:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'TEST': {
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }
}

This ensures tests never touch your development database.
"""
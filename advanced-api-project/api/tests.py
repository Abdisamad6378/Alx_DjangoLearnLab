"""
Unit Tests for Book API
=======================
Task 3: Comprehensive test suite covering CRUD, filtering, searching, ordering, and permissions.
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
    """
    Test case for Book API endpoints.
    Tests CRUD operations, filtering, searching, ordering, and permissions.
    """
    
    def setUp(self):
        """Set up test data before each test."""
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='John Smith')
        self.author2 = Author.objects.create(name='Jane Doe')
        self.author3 = Author.objects.create(name='Bob Johnson')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Python Programming',
            publication_year=2021,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Advanced Python',
            publication_year=2022,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='Django for Beginners',
            publication_year=2020,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title='Django REST Framework',
            publication_year=2023,
            author=self.author2
        )
        self.book5 = Book.objects.create(
            title='JavaScript Basics',
            publication_year=2019,
            author=self.author3
        )
        
        # API client and URLs
        self.client = APIClient()
        self.books_list_url = '/api/books/'
        self.book_detail_url = lambda pk: f'/api/books/{pk}/'
        self.book_create_url = '/api/books/create/'
        self.book_update_url = lambda pk: f'/api/books/update/{pk}/'
        self.book_delete_url = lambda pk: f'/api/books/delete/{pk}/'

    # ======================================================================
    # CRUD OPERATIONS TESTS
    # ======================================================================

    def test_01_create_book_authenticated(self):
        """Test creating a book as authenticated user."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Test Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 6)

    def test_02_create_book_unauthenticated(self):
        """Test creating a book as unauthenticated user."""
        data = {
            'title': 'Test Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_03_create_book_invalid_data(self):
        """Test creating a book with invalid data."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Test',
            'publication_year': datetime.now().year + 10,
            'author': 99999
        }
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_04_retrieve_all_books(self):
        """Test retrieving list of all books."""
        response = self.client.get(self.books_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_05_retrieve_single_book(self):
        """Test retrieving a single book by ID."""
        response = self.client.get(self.book_detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_06_retrieve_nonexistent_book(self):
        """Test retrieving a non-existent book."""
        response = self.client.get(self.book_detail_url(99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_07_update_book_authenticated(self):
        """Test updating a book as authenticated user."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Title',
            'publication_year': 2024,
            'author': self.author2.id
        }
        response = self.client.put(self.book_update_url(self.book1.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_08_update_book_unauthenticated(self):
        """Test updating a book as unauthenticated user."""
        data = {'title': 'Hacked Title'}
        response = self.client.put(self.book_update_url(self.book1.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_09_partial_update_book(self):
        """Test partially updating a book (PATCH)."""
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Partially Updated'}
        response = self.client.patch(self.book_update_url(self.book1.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated')

    def test_10_delete_book_authenticated(self):
        """Test deleting a book as authenticated user."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.book_delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.count(), 4)

    def test_11_delete_book_unauthenticated(self):
        """Test deleting a book as unauthenticated user."""
        response = self.client.delete(self.book_delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_12_delete_nonexistent_book(self):
        """Test deleting a non-existent book."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.book_delete_url(99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ======================================================================
    # FILTERING TESTS
    # ======================================================================

    def test_13_filter_by_title_exact(self):
        """Test filtering by exact title match."""
        response = self.client.get(self.books_list_url, {'title': 'Python Programming'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_14_filter_by_title_contains(self):
        """Test filtering by title containing text."""
        response = self.client.get(self.books_list_url, {'title__icontains': 'python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_15_filter_by_author_exact(self):
        """Test filtering by exact author name."""
        response = self.client.get(self.books_list_url, {'author__name': 'John Smith'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_16_filter_by_author_contains(self):
        """Test filtering by author name containing text."""
        response = self.client.get(self.books_list_url, {'author__name__icontains': 'john'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_17_filter_by_year_exact(self):
        """Test filtering by exact publication year."""
        response = self.client.get(self.books_list_url, {'publication_year': 2021})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_18_filter_by_year_range(self):
        """Test filtering by year range."""
        response = self.client.get(self.books_list_url, {
            'publication_year__gte': 2020,
            'publication_year__lte': 2022
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_19_filter_multiple_criteria(self):
        """Test filtering with multiple criteria."""
        response = self.client.get(self.books_list_url, {
            'author__name__icontains': 'john',
            'publication_year__gte': 2021
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ======================================================================
    # SEARCHING TESTS
    # ======================================================================

    def test_20_search_by_title(self):
        """Test searching by title."""
        response = self.client.get(self.books_list_url, {'search': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_21_search_by_author(self):
        """Test searching by author name."""
        response = self.client.get(self.books_list_url, {'search': 'Smith'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_22_search_partial_match(self):
        """Test searching with partial text."""
        response = self.client.get(self.books_list_url, {'search': 'djan'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_23_search_case_insensitive(self):
        """Test search is case-insensitive."""
        response = self.client.get(self.books_list_url, {'search': 'PYTHON'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_24_search_no_results(self):
        """Test search with no matches."""
        response = self.client.get(self.books_list_url, {'search': 'nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # ======================================================================
    # ORDERING TESTS
    # ======================================================================

    def test_25_order_by_title_asc(self):
        """Test ordering by title ascending."""
        response = self.client.get(self.books_list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_26_order_by_title_desc(self):
        """Test ordering by title descending."""
        response = self.client.get(self.books_list_url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))

    def test_27_order_by_year_asc(self):
        """Test ordering by year ascending."""
        response = self.client.get(self.books_list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))

    def test_28_order_by_year_desc(self):
        """Test ordering by year descending."""
        response = self.client.get(self.books_list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    # ======================================================================
    # COMBINED FEATURES TESTS
    # ======================================================================

    def test_29_filter_search_order_combined(self):
        """Test combining filter, search, and order."""
        response = self.client.get(self.books_list_url, {
            'search': 'python',
            'publication_year__gte': 2021,
            'ordering': '-publication_year'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ======================================================================
    # PERMISSIONS TESTS
    # ======================================================================

    def test_30_read_access_unauthenticated(self):
        """Test unauthenticated users can read."""
        response = self.client.get(self.books_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.book_detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_31_write_access_authenticated(self):
        """Test authenticated users can write."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.book_create_url, {
            'title': 'Auth Test',
            'publication_year': 2024,
            'author': self.author1.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # ======================================================================
    # MODEL TESTS
    # ======================================================================

    def test_32_book_str_method(self):
        """Test Book string representation."""
        expected = f"{self.book1.title} by {self.book1.author.name}"
        self.assertEqual(str(self.book1), expected)

    def test_33_author_str_method(self):
        """Test Author string representation."""
        self.assertEqual(str(self.author1), self.author1.name)

    def test_34_book_ordering(self):
        """Test default book ordering."""
        books = Book.objects.all()
        titles = [book.title for book in books]
        self.assertEqual(titles, sorted(titles))

    # ======================================================================
    # EDGE CASES
    # ======================================================================

    def test_35_create_book_future_year(self):
        """Test creating book with future year."""
        self.client.force_authenticate(user=self.user)
        future_year = datetime.now().year + 10
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.post(self.book_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_36_create_book_missing_fields(self):
        """Test creating book with missing required fields."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.book_create_url, {
            'title': 'Missing Fields'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
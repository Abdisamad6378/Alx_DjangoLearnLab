"""
URL Configuration for Book API
==============================
Task 1 & 2: URL patterns for all views
"""

from django.urls import path
from . import views

urlpatterns = [
    # List and Detail Views (Read-only)
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Create View
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    
    # Update View
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    
    # Delete View
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]

# URL Patterns Summary:
# ----------------------
# GET    /api/books/           - List all books (with filter/search/order)
# GET    /api/books/<id>/      - Retrieve single book
# POST   /api/books/create/    - Create new book (auth required)
# PUT    /api/books/<id>/update/ - Update book (auth required)
# DELETE /api/books/<id>/delete/ - Delete book (auth required)
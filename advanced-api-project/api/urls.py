from django.urls import path
from . import views

urlpatterns = [
    # List and Detail Views
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Create View
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    
    # Update View - NOTE: 'update' comes BEFORE the ID
    path('books/update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),
    
    # Delete View - NOTE: 'delete' comes BEFORE the ID
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),
]
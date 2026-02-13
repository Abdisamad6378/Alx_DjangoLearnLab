from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router for AuthorViewSet
router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet)

urlpatterns = [
    # Book endpoints
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Author endpoints from router
    path('', include(router.urls)),
]
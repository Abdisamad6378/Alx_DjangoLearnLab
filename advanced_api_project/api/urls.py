from django.urls import path
from .views import (
    ListView,      # ← Changed from BookList
    DetailView,     # ← Changed from BookDetail
    CreateView,     # ← Changed from BookCreate
    UpdateView,     # ← Changed from BookUpdate
    DeleteView      # ← Changed from BookDelete
)

urlpatterns = [
    path('books/', ListView.as_view(), name='book-list'),
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),
    path('books/create/', CreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', UpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book-delete'),
]
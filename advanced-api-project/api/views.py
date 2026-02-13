"""
Custom Views with Filtering, Searching, and Ordering
=====================================================
Task 1: Generic Views for CRUD operations
Task 2: Filtering, Searching, and Ordering
Task 3: Unit Tests (implemented in tests.py)
"""

from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from .models import Book
from .serializers import BookSerializer


class BookFilter(django_filters.FilterSet):
    """
    Custom FilterSet for Book model with advanced filtering options.
    """
    title_contains = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='icontains',
        help_text="Title contains (case-insensitive)"
    )
    author_name_contains = django_filters.CharFilter(
        field_name='author__name', 
        lookup_expr='icontains',
        help_text="Author name contains (case-insensitive)"
    )
    year_min = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gte',
        help_text="Minimum publication year"
    )
    year_max = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lte',
        help_text="Maximum publication year"
    )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'author__name': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
        }


# ======================================================================
# Task 1: Generic Views for CRUD Operations
# ======================================================================

class BookListView(generics.ListAPIView):
    """
    List all books with filtering, searching, and ordering.
    
    URL: /api/books/
    Method: GET
    Permissions: AllowAny (read-only for everyone)
    
    Features:
    - Filtering by title, author, publication_year
    - Searching in title and author name
    - Ordering by title, publication_year, author
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Filter backends
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    
    # Filtering configuration
    filterset_class = BookFilter
    
    # Searching configuration
    search_fields = ['title', 'author__name']
    
    # Ordering configuration
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single book by ID.
    
    URL: /api/books/<int:pk>/
    Method: GET
    Permissions: AllowAny
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    Create a new book.
    
    URL: /api/books/create/
    Method: POST
    Permissions: IsAuthenticated
    
    Features:
    - Validates input data
    - Returns created book on success
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Custom create method for additional logic.
        """
        print(f"Book created by user: {self.request.user}")
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method with enhanced response.
        """
        response = super().create(request, *args, **kwargs)
        response.data['message'] = 'Book created successfully!'
        return response


class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book.
    
    URL: /api/books/<int:pk>/update/
    Method: PUT, PATCH
    Permissions: IsAuthenticated
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        print(f"Book updated by user: {self.request.user}")
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Book updated successfully!',
            'book': serializer.data
        })


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book.
    
    URL: /api/books/<int:pk>/delete/
    Method: DELETE
    Permissions: IsAuthenticated
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_destroy(self, instance):
        print(f"Book deleted by user: {self.request.user}")
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Book deleted successfully!'}, 
            status=status.HTTP_200_OK
        )
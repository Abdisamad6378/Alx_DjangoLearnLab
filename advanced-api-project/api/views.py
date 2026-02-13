from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated  # ← THIS LINE MUST BE EXACT
from django_filters import rest_framework as django_filters
from .models import Book
from .serializers import BookSerializer
from datetime import datetime


class BookFilter(django_filters.FilterSet):
    title_contains = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='icontains'
    )
    author_name_contains = django_filters.CharFilter(
        field_name='author__name', 
        lookup_expr='icontains'
    )
    year_min = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gte'
    )
    year_max = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lte'
    )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'author__name': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
        }


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # ← READ-ONLY FOR ALL
    
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # ← READ-ONLY FOR ALL


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # ← ONLY AUTHENTICATED
    
    def perform_create(self, serializer):
        print(f"Book created by user: {self.request.user}")
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # ← ONLY AUTHENTICATED
    
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
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # ← ONLY AUTHENTICATED
    
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
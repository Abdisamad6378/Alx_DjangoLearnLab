"""
Custom Serializers for Book API
===============================
Task 0: Custom serializers with nested relationships and validation
"""

from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model with custom validation.
    
    Features:
    - All Book fields
    - Read-only author_name field
    - Custom validation for publication_year (no future years)
    - Object-level validation
    """
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'author_name']
    
    def validate_publication_year(self, value):
        """
        Custom validation: publication_year cannot be in the future.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value
    
    def validate(self, data):
        """
        Object-level validation example.
        """
        title = data.get('title')
        if title and len(title) < 3:
            raise serializers.ValidationError(
                {"title": "Title must be at least 3 characters long."}
            )
        return data


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model with nested books.
    
    Features:
    - Author name field
    - Nested BookSerializer to show all books by this author
    - Computed book_count field
    """
    books = BookSerializer(many=True, read_only=True)
    book_count = serializers.IntegerField(source='books.count', read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'book_count', 'books']
    
    def to_representation(self, instance):
        """
        Customize the representation.
        """
        representation = super().to_representation(instance)
        representation['description'] = f"Author {instance.name} has written {instance.books.count()} books"
        return representation
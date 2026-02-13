from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    Includes all Book fields and adds custom validation
    to ensure publication_year is not in the future.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation to prevent future publication years.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            ValidationError: If the year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    
    Includes:
        - name: The author's name
        - books: Nested BookSerializer to show all books by this author
                 This demonstrates handling nested relationships.
    
    The nested books field is read-only and shows how to serialize
    related objects dynamically.
    """
    # Nested serializer to display all books by this author
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
    
    def to_representation(self, instance):
        """
        Customize the representation to include book count.
        
        This shows how to add computed fields to serialized output.
        """
        representation = super().to_representation(instance)
        representation['book_count'] = instance.books.count()
        return representation
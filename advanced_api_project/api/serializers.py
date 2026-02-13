from rest_framework import serializers
from .models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'publication_year']
    
    def validate_publication_year(self, value):
        if value > 2026:
            raise serializers.ValidationError("Publication year cannot be in the future")
        return value
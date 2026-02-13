from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin configuration for Author model"""
    list_display = ('id', 'name', 'book_count')
    search_fields = ('name',)
    
    def book_count(self, obj):
        """Display number of books by this author in admin"""
        return obj.books.count()
    book_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model"""
    list_display = ('id', 'title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author__name')
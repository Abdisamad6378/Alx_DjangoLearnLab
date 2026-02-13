"""
Models for Book API
===================
Task 0: Setting Up Django Project with Custom Serializers
"""

from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    Fields:
        name: The author's full name
    """
    name = models.CharField(max_length=100, db_index=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing a book with its details.
    
    Fields:
        title: The book's title
        publication_year: Year the book was published
        author: ForeignKey linking to Author (one-to-many relationship)
    """
    title = models.CharField(max_length=200, db_index=True)
    publication_year = models.IntegerField(db_index=True)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books'
    )
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['publication_year']),
            models.Index(fields=['author', 'publication_year']),
        ]
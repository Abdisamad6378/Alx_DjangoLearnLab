from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    Fields:
        name (CharField): The author's full name
    """
    name = models.CharField(max_length=100, help_text="Author's full name")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing a book with its details.
    
    Fields:
        title (CharField): The book's title
        publication_year (IntegerField): Year the book was published
        author (ForeignKey): Reference to the Author model (one-to-many relationship)
    """
    title = models.CharField(max_length=200, help_text="Book title")
    publication_year = models.IntegerField(help_text="Year of publication")
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        help_text="Author who wrote this book"
    )
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['title']
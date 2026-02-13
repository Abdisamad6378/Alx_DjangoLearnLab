from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)  # Simple CharField for ALX tests
    publication_year = models.IntegerField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
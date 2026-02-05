from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(
        Author, 
        
        on_delete=models.CASCADE,
        related_name='author'
    )
    

class library(models.Model):
    title = models.CharField(max_length=40)
    book = models.ManyToManyField(
        Book,
        related_name = 'LIbrary'
    )
    
    class Librarian(models.Model):
        name = models.CharField(max_length=30)
        Library= models.OneToOneField(
            library,
            realted_name = 'librarian'
        )
        
from django.shortcuts import render
from models import Book
# Create your views here.
def list_books(request):
    books = Book.objects.all()
    context = {'list_books,:authors'}
    return render(request, 'authors/list_books.html' , context)
from django.shortcuts import render
from django.views.generic import DetailView
from models import Book
from .models import library
# Create your views here.
def list_books(request):
    books = Book.objects.all()
    context = {'list_books,:authors'}
    return render(request, 'relationship_app/list_books.html' , context)

class libraryDeltaview(DetailView):
    model = library
    template_name = 'books/library_detail.html'
    
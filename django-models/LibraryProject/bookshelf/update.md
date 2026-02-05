from bookshelf.models import Book book = Book.objects.get(pk=1), book.title="Nineteen Eighty-Four", book.save()
#Nineteen Eighty-Four
from django.contrib import admin
from .models import Book
# Register your models here.
class Bookadmin(admin.ModelAdmin):
    list_display = ('title','author','publication_year')
    list_filter = ('title','author','publication_year')
    search_fields = ('title','author')
admin.site.register(Book)
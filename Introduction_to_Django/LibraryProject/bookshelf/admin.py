from django.contrib import admin
from .models import Book
# Register your models here.
class Bookadmin(admin.ModelAdmin):
    list_display = ('title','author','publication_year')
admin.site.register(Book)

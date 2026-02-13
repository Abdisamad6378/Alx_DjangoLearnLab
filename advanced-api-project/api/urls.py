from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for automatic URL routing
router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet)
router.register(r'books', views.BookViewSet)

# The router automatically generates URLs for all CRUD operations
urlpatterns = [
    path('', include(router.urls)),
]
from django.shortcuts import render

# import class yang dibutuhkan untuk membuat view
from django.http import Http404
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView

# import Book model dan class seriallizers untuk modul Book
from .models import Book
from .seriallizers import BookListSerializer, BookDetailSerializer



# Membuat View untuk API endpoint "Get All Books"
# /api/book
class BookListView(ListAPIView):
   # Mengset class serializer
   serializer_class = BookListSerializer
   queryset = Book.objects.all()
   # Menambahkan  Fitur filtering, Searching dan ordering
   filter_backends = (
      DjangoFilterBackend,
      SearchFilter,
      OrderingFilter
   )
   # Mengset fields/kolom untuk fitur filtering
   filter_fields = ['author']
   # Mengset field/kolom untuk fitur searching
   search_fields = ['title', 'author']
   # Mengset field/kolom untuk fitur ordering
   ordering_fields = ['title', 'stock', 'price', 'created_at']
   # Mengset field/kolom default ordering
   ordering = ['created_at']
   
   
# Membuat View untuk API endpoint "Get Detail of Book"
# /api/book/:id
class BookDetailView(RetrieveAPIView):
   # Mengset class serializer
   serializer_class = BookDetailSerializer
   queryset = Book.objects.all()


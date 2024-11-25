from django.shortcuts import render

# import class yang dibutuhkan untuk membuat view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics 

# import Book model dan class seriallizers untuk modul Book
from .models import Book, Transaction
from .seriallizers import BookSerializer, TransactionSerializer, TransactionDetailSerializer



# Membuat View untuk API endpoint "Get All Books"
# GET:/api/book
class BookListView(generics.ListAPIView):
   # Mengset class serializer
   serializer_class = BookSerializer
   queryset = Book.objects.all()
   
   # Menambahkan  Fitur filtering, Searching dan ordering
   filter_backends = (
      DjangoFilterBackend,
      SearchFilter,
      OrderingFilter
   )
   
   # Mengset fields/kolom untuk fitur filtering
   filterset_fields = ['author']
   # Mengset field/kolom untuk fitur searching
   search_fields = ['title', 'author']
   # Mengset field/kolom untuk fitur ordering
   ordering_fields = ['title', 'stock', 'price', 'created_at']
   # Mengset field/kolom default ordering
   ordering = ['created_at']
   
   def get(self, request, *args, **kwargs):
      # Gunakan self.filter_queryset untuk mempertahankan fitur filter, search, dan ordering
      queryset = self.filter_queryset(self.get_queryset())
      serializer = self.get_serializer(queryset, many=True)

      # Cek apakah data kosong
      if not queryset.exists():
         return Response({
               "message": "No books found or Please add some books.",
               "data": []
         }, status=status.HTTP_200_OK)

      # Kembalikan response dengan data
      return Response({
         "message": "Books retrieved successfully",
         "data": serializer.data
      }, status=status.HTTP_200_OK)
   

   
# Membuat View untuk API endpoint "Get Detail of Book"
# View ini digunakan untuk get book by id,(update) put & patch book, dan delete book 
# GET:/api/book/:id
# PUT:/api/book/:id
# PATCH:/api/book/:id
# DELETE:/api/book/:id
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
   # Mengset class serializer
   serializer_class = BookSerializer
   queryset = Book.objects.all()
   
   # Menambahkan Response
   def get_object(self):
      # Ambil primary key dari URL
      pk = self.kwargs.get('pk')
      
      # Cek apakah objek ada di database
      try:
         book = Book.objects.get(pk=pk)
         return book
      except Book.DoesNotExist:
         # Jika objek tidak ditemukan, kita lempar exception dengan pesan kustom
         raise NotFound("Book with the given ID was not found.")

   def get(self, request, *args, **kwargs):
      book = self.get_object()
      return Response({
         "message": "Book details retrieved successfully",
         "data": BookSerializer(book).data
      })

   def put(self, request, *args, **kwargs):
      book = self.get_object()
      serializer = self.get_serializer(book, data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response({
               "message": "Data successfully updated",
               "data": serializer.data
         })
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   def patch(self, request, *args, **kwargs):
      book = self.get_object()
      serializer = self.get_serializer(book, data=request.data, partial=True)
      if serializer.is_valid():
         serializer.save()
         return Response({
               "message": "Data successfully updated by patch",
               "data": serializer.data
         })
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   def delete(self, request, *args, **kwargs):
      book = self.get_object()
      book.delete()
      return Response({"message": "Data successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

   
   
# Membuat View untuk API endpoint "Create book"
# POST:/api/book
class BookCreateView(generics.CreateAPIView):
   serializer_class = BookSerializer
   queryset = Book.objects.all()
   
   def post(self, request, *args, **kwargs):
     serializer = self.get_serializer(data=request.data)
     if serializer.is_valid():
        serializer.save()
        return Response({
           "message": "Book Successfully created",
           "data": serializer.data,
        }, status=status.HTTP_201_CREATED)

     return Response({
        "error": "Invalid data",
        "detail": serializer.errors
     }, status=status.HTTP_400_BAD_REQUEST)
     

# Membuat View untuk API endpoint "Create Transaction"
# POST:/api/transactions
class TransactionCreateView(generics.CreateAPIView):
   serializer_class = TransactionSerializer
   queryset = Transaction.objects.all()

   def create(self, request, *args, **kwargs):
         serializer = self.get_serializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         transaction = serializer.save()  # Memanggil `create` di serializer
         
         # Buat pesan respons di sini
         return Response({
               "message": "Transaction successfully created",
               "data": TransactionSerializer(transaction).data
         }, status=status.HTTP_201_CREATED)
   
         
# Membuat View untuk API endpoint "Get Transaction" 
# GET:/api/transactions/:id
class TransactionDetailView(generics.RetrieveAPIView):
   serializer_class = TransactionDetailSerializer
   queryset = Transaction.objects.all()
   
    # Menambahkan Response
   def get_object(self):
      # Ambil primary key dari URL
      pk = self.kwargs.get('pk')
      
      # Cek apakah objek ada di database
      try:
         transaction = Transaction.objects.get(pk=pk)
         return transaction
      except Transaction.DoesNotExist:
         # Jika objek tidak ditemukan, kita lempar exception dengan pesan kustom
         raise NotFound("Transaction with the given ID was not found.")
      
   def get(self, request, *args, **kwargs):
      transaction = self.get_object()
      return Response({
         "message": "Transaction details retrieved successfully",
         "data": TransactionSerializer(transaction).data
         })



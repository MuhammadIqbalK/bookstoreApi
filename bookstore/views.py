from datetime import datetime
from django.shortcuts import render

# import class yang dibutuhkan untuk membuat view
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.views import APIView
# import class untuk autentikasi jwt
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken

from .filters import TransactionFilter
# import model dan class seriallizers untuk semua modul
from .models import Book, Transaction, User
from .seriallizers import (BookSerializer, TransactionSerializer, TransactionDetailSerializer, 
                           MyTokenObtainPairSerializer, RegisterSerializer, ChangePasswordSerializer,
                           UserSerializer)
from rest_framework.permissions import AllowAny




# Membuat view untuk API endpoint "Register"
# POST:/api/register/
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



# Membuat View untuk memodifikasi ObtainTokenPairView menjadi API endpoint "Login"
# POST:/api/login/
class CustomLoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data['message'] = 'Login successful!.'
        return response



# Custom View untuk memodifikasi Token refresh agar menghasilkan token refresh
# POST:/api/login/refresh/
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except InvalidToken as e:
            return Response({"detail": str(e)}, status=400)


    
# Membuat View untuk API endpoint "Logout" dan memblacklist token
# POST:/api/logout/
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.logout_at = timezone.now()
        user.save()

        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
     
     
# Membuat View untuk API endpoint "Change passsword"
# PUT:/api/users/:id /change_password/    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save the new password
        serializer.update(user, serializer.validated_data)

        # Optional: Update logout_at to force re-login
        user.logout_at = datetime.now()
        user.save()

        return Response(
            {"message": "Password updated successfully. Please login again."},
            status=status.HTTP_200_OK
        )
     
      
 # Membuat View untuk API endpoint "Update User"
 # PATCH:/api/users/:id/update/   
class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is trying to update their own profile
        if request.user.pk != user.pk:
            return Response(
                {"authorize": "You don't have permission to update this user."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Create the serializer with context including request
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Data successfully updated.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
     
 # Membuat View untuk API endpoint "Update User"
 # GET:/api/users/:id  
class GetUserByIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Pastikan pengguna hanya bisa mengakses profil mereka sendiri atau admin
        if request.user.pk != user.pk and not request.user.is_staff:
            return Response(
                {"error": "You don't have permission to view this user's profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = UserSerializer(user)
        return Response({
           "message": "User details retrieved successfully.",
           "data": serializer.data}, status=status.HTTP_200_OK)

     
# Membuat View untuk API endpoint "Get All Books"
# GET:/api/book/all
class BookListView(generics.ListAPIView):
   # Mengset class serializer
   serializer_class = BookSerializer
   queryset = Book.objects.all()
   # mengset autentikasi
   permission_classes = [IsAuthenticated]

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
      # terapkan pagination
      page = self.paginate_queryset(queryset) 

      # Cek apakah data kosong
      if not queryset.exists():
         return Response({
               "message": "No books found or Please add some books.",
               "data": []
         }, status=status.HTTP_200_OK)
         
      if page is not None:  # Paginated response
               serializer = self.get_serializer(page, many=True)
               return self.get_paginated_response({
                  "message": "Book retrieved successfully.",
                  "data": serializer.data
               })

      # respon jika pagination tidak ada
      serializer = self.get_serializer(queryset, many=True)
      return Response({
         "message": "Books retrieved successfully.",
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
         "message": "Book details retrieved successfully.",
         "data": BookSerializer(book).data
      })

   def put(self, request, *args, **kwargs):
      book = self.get_object()
      serializer = self.get_serializer(book, data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response({
               "message": "Data successfully updated.",
               "data": serializer.data
         })
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   def patch(self, request, *args, **kwargs):
      book = self.get_object()
      serializer = self.get_serializer(book, data=request.data, partial=True)
      if serializer.is_valid():
         serializer.save()
         return Response({
               "message": "Data successfully updated by patch.",
               "data": serializer.data
         })
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   def delete(self, request, *args, **kwargs):
      book = self.get_object()
      book.delete()
      return Response({"message": "Data successfully deleted."}, status=status.HTTP_204_NO_CONTENT)

   
   
# Membuat View untuk API endpoint "Create book"
# POST:/api/book/
class BookCreateView(generics.CreateAPIView):
   serializer_class = BookSerializer
   queryset = Book.objects.all()
   
   def post(self, request, *args, **kwargs):
     serializer = self.get_serializer(data=request.data)
     if serializer.is_valid():
        serializer.save()
        return Response({
           "message": "Book Successfully created.",
           "data": serializer.data,
        }, status=status.HTTP_201_CREATED)

     return Response({
        "error": "Invalid data",
        "detail": serializer.errors
     }, status=status.HTTP_400_BAD_REQUEST)
     


# Membuat View untuk API endpoint "Create Transaction"
# POST:/api/transactions/
class TransactionCreateView(generics.CreateAPIView):
   permission_classes = [IsAuthenticated]
   serializer_class = TransactionSerializer
   queryset = Transaction.objects.all()

   def create(self, request, *args, **kwargs):
         serializer = self.get_serializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         transaction = serializer.save()  # Memanggil `create` di serializer
         
         # Buat pesan respons di sini
         return Response({
               "message": "Transaction successfully created.",
               "data": TransactionSerializer(transaction).data
         }, status=status.HTTP_201_CREATED)
  
  
         
 # Membuat View Untuk API endpoint "Get All transaction" 
 # GET:/api/transatcions       
class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
      DjangoFilterBackend,
      OrderingFilter
   )
    # Custom filter by date range
    filterset_class = TransactionFilter
    
    ordering_fields = ['transaction_date', 'total_amount']
    ordering = ['transaction_date']
   
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)
   
    def get(self, *args, **kwargs):
         queryset = self.filter_queryset(self.get_queryset())  # Retain filtering
         page = self.paginate_queryset(queryset)  # Apply pagination

         if not queryset.exists():
               return Response({
                  "message": "No Transaction found.",
                  "data": []
               }, status=status.HTTP_200_OK)

         if page is not None:  # Paginated response
               serializer = self.get_serializer(page, many=True)
               return self.get_paginated_response({
                  "message": "Transactions retrieved successfully.",
                  "data": serializer.data
               })

         # Non-paginated response (fallback)
         serializer = self.get_serializer(queryset, many=True)
         return Response({
               "message": "Transactions retrieved successfully.",
               "data": serializer.data
         }, status=status.HTTP_200_OK)
   
   
 
# Membuat View untuk API endpoint "Get Transaction" 
# GET:/api/transactions/:id
class TransactionDetailView(generics.RetrieveAPIView):
   serializer_class = TransactionSerializer
   permission_classes = [IsAuthenticated]

   def get_queryset(self):
      user = self.request.user
      return Transaction.objects.filter(user=user)

   def get(self, request, *args, **kwargs):
      try:
            transaction = self.get_object()
            return Response({
               "message": "Transaction retrieved successfully.",
               "data": self.get_serializer(transaction).data
            }, status=status.HTTP_200_OK)
      except Transaction.DoesNotExist:
            return Response(
               {"error": "Transaction not found."},
               status=status.HTTP_404_NOT_FOUND
            )



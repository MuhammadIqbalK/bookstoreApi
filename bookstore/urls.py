from django.urls import path

# import semua class View modul Book
from .views import (BookListView, BookDetailView, BookCreateView,TransactionListView, TransactionCreateView, TransactionDetailView, 
                    CustomLoginView, RegisterView, LogoutView, CustomTokenRefreshView, ChangePasswordView, 
                    UpdateUserView, GetUserByIdView)


urlpatterns = [
    # Membuat Route untuk Api endpoint book
     path('book/all/',BookListView.as_view(), name='api-book-list'),
     path('book/<int:pk>', BookDetailView.as_view(), name='api-book-detail-update-delete'),
     path('book/',BookCreateView.as_view(), name='api-book-create'),
    # Membuat Route untuk Api endpoint Transaction
     path('transactions/',TransactionCreateView.as_view(), name='api-transaction-create'),
     path('transactions/all/',TransactionListView.as_view(), name='api-transaction-list'),
     path('transactions/<int:pk>',TransactionDetailView.as_view(), name='api-transaction-detail'),
    # Membuat Route untuk Api endpoint Authentication
     path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
     path('login/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
     path('logout/', LogoutView.as_view(), name='api-logout'),
     path('register/', RegisterView.as_view(), name='api-register'),
     path('users/<int:pk>/change-password/', ChangePasswordView.as_view(), name='api-change-user-password'),
     path('users/<int:pk>/update/', UpdateUserView.as_view(), name='api-user-update'),
     path('users/<int:pk>', GetUserByIdView.as_view(), name='api-user-detail'),
          
]

from django.urls import path

# import semua class View modul Book
from .views import (BookListView, BookDetailView, BookCreateView, TransactionCreateView, TransactionDetailView, 
                    CustomLoginView, RegisterView, LogoutView, CustomTokenRefreshView)


urlpatterns = [
    # Membuat Route untuk Api endpoint book
     path('book/all/',BookListView.as_view(), name='api-book-list'),
     path('book/<int:pk>', BookDetailView.as_view(), name='api-book-detail-update-delete'),
     path('book/',BookCreateView.as_view(), name='api-book-create'),
    # Membuat Route untuk Api endpoint Transaction
     path('transactions/',TransactionCreateView.as_view(), name='api-transaction-create'),
     path('transactions/<int:pk>',TransactionDetailView.as_view(), name='api-transaction-detail'),
    # Membuat Route untuk Api endpoint Authentication
     path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
     path('login/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
     path('logout/', LogoutView.as_view(), name='api-logout'),
     path('register/', RegisterView.as_view(), name='api-register'),

]

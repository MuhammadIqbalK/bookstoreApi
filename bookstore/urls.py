from django.urls import path


# import semua class View modul Book
from .views import BookListView, BookDetailView, BookCreateView, TransactionCreateView, TransactionDetailView


urlpatterns = [
    # Membuat Route untuk Api endpoint book
     path('book/all/',BookListView.as_view(), name='api-book-list'),
     path('book/<int:pk>', BookDetailView.as_view(), name='api-book-detail-update-delete'),
     path('book/',BookCreateView.as_view(), name='api-book-create'),
     path('transactions/',TransactionCreateView.as_view(), name='api-transaction-create'),
     path('transactions/<int:pk>',TransactionDetailView.as_view(), name='api-transaction-detail')
]

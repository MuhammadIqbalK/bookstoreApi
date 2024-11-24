from django.urls import path


# import semua class View modul Book
from .views import BookListView, BookDetailView, BookCreateView


urlpatterns = [
    # Membuat Route untuk Api endpoint book
     path('book/all/',BookListView.as_view(), name='api-book-list'),
     path('book/<int:pk>', BookDetailView.as_view(), name='api-book-detail'),
     path('book/',BookCreateView.as_view(), name='api-book-create'),
]

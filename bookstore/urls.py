from django.urls import path


# import semua class View modul Book
from .views import BookListView, BookDetailView


urlpatterns = [
    # Membuat Route untuk Api endpoint book
     path('book/',BookListView.as_view(), name='api-book-list'),
     path('book/<int:pk>', BookDetailView.as_view(), name='api-book-detail'),
     
]

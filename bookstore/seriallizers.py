# import class serializers
from rest_framework.serializers import ModelSerializer

# import Book model
from .models import Book


# Membuat class serializers untuk semua API endpoint "book"
class BookSerializer(ModelSerializer):
   class Meta:
      model = Book
      fields = ('id', 'title', 'author', 'price', 'stock')



 

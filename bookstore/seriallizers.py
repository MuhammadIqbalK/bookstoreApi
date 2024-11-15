# import class serializers
from rest_framework.serializers import ModelSerializer

# import Book model
from .models import Book


# Membuat class serializers untuk API endpoint "Get list all book"
class BookListSerializer(ModelSerializer):
   class Meta:
      model = Book
      fields = ('id', 'title', 'author', 'price', 'stock')

# Membuat class serializers untuk API endpoint "Get detail book"
class BookDetailSerializer(ModelSerializer):
   class Meta:
      model = Book
      fields = ('id', 'title', 'author', 'price', 'stock', 'created_at')


 

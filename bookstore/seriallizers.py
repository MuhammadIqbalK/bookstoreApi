# import class serializers
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.utils import timezone
from django.db import transaction

# import Book model
from .models import User, Book, Transaction, TransactionItem



# Membuat class serializers untuk semua API endpoint "book"
class BookSerializer(ModelSerializer):
   class Meta:
      model = Book
      fields = ('id', 'title', 'author', 'price', 'stock')


# Membuat class Serializers untuk transactionItem
class TransactionItemSerializer(ModelSerializer):
   class Meta:
      model = TransactionItem
      fields = ['book', 'quantity', 'price_total']
      # jika read_only_fields artinya tidak akan keluar di body request
      read_only_fields = ['price_total'] 
 
 
# Membuat class Serializers untuk Api endpoint "get:/Transaction/:id"   
class TransactionDetailSerializer(ModelSerializer):
   user_email = serializers.CharField(source='user.email', read_only=True)
   items = TransactionItemSerializer(many=True)
   
   class Meta:
      model = Transaction
      fields = ('id', 'transaction_date', 'total_amount', 'user_email', 'items' )


# Membuat class serializer untuk Api endpoint "Post:/Transaction"
class TransactionSerializer(ModelSerializer):
   user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
   items = TransactionItemSerializer(many=True)
   
   class Meta:
      model = Transaction
      fields = ['id','transaction_date', 'total_amount', 'user', 'items']
      read_only_fields = ['id', 'transaction_date', 'total_amount']
     
   #menjaga transaksi agar bersifat atomic (berhasil atau gagal secara keseluruhan)  
   @transaction.atomic
   def create(self, validated_data):
      # Memvalidasi items dari body request
      items_data = validated_data.pop('items')
      # Memvalidasi user dari body request
      user = validated_data['user']
      
      #create/buat transaction baru
      transaction = Transaction.objects.create(transaction_date=timezone.now(), total_amount=0, user=user)
      total_amount = 0
      
      for item_data in items_data:
         book = item_data['book']
         quantity = item_data['quantity']
         
         # validasi untuk mengecek ketersediaan stock book
         if book.stock < quantity:
            raise serializers.ValidationError(f"Not enough stock for {book.title}")

         # kalkulasi total harga atau total_amount
         price_total = book.price * quantity
         total_amount += price_total
         
         # create/buat transaction_item
         TransactionItem.objects.create(quantity=quantity, price_total=price_total, book=book, transaction=transaction)
      
         #kurangi stock book
         book.stock -= quantity
         book.save()
      
      #update total_amount transaction
      transaction.total_amount = total_amount
      transaction.save()
   
      return transaction
      
      

      
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

 

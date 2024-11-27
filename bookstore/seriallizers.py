# import class serializers
from datetime import datetime
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.utils import timezone
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


# import Book model
from .models import User, Book, Transaction, TransactionItem, User


# Membuat class serializer untuk TokenObtainPairSerializer(login menggunakan jwt)
# berguna untuk menambahkan informasi tambahan di paylooad seperti username (* opsional)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['iat'] = int(datetime.now().timestamp())  # Menambahkan 'iat'
        token['logout_at'] = None  # Masih belum logout
        return token

     
# Membut class serializer untuk endpoint logout dan memblacklist refresh token    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs.get('refresh')
        try:
            token = RefreshToken(refresh)
            # Blacklist refresh token
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError(f"Invalid refresh token: {str(e)}")
        return attrs     
     
     

# Membuat class serializer untuk API endpoint "Register"
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'phone_number', 'birth_date')
        extra_kwargs = {
            'phone_number': {'required': True},
            'birth_date': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            birth_date=validated_data['birth_date']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


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
   
   
   
      
      

      
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

 

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
class RegisterSerializer(ModelSerializer):
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


# Membuat Class Serializers Untuk Api endpoint change-password
class ChangePasswordSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('password', 'password2','old_password')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
                                              
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value
    
    def update(self, instance, validated_data):
        
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
    

# Membuat Class Serializer untuk Api endpoint "user update"
class UserSerializer(ModelSerializer):
    email = serializers.EmailField(required=False)  # Jadikan opsional
    username = serializers.CharField(required=False)  # Jadikan opsional

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'birth_date')

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        
        # Update only the fields present in validated_data
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)

        instance.save()
        return instance


    
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
     
  # Validasi apakah ID user valid.   
   def validate_user(self, value):
        if not User.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError(f"Invalid user ID '{value.id}'. User does not exist.")
        return value

 # Validasi apakah ID book valid dan quantity tidak bernilai 0 atau kurang.
   def validate_items(self, value):
        invalid_books = []
        invalid_quantities = []
        
        for index, item in enumerate(value):
            book_id = item.get('book')
            quantity = item.get('quantity', 0)
            
            # Validasi ID buku
            if not Book.objects.filter(pk=book_id).exists():
                invalid_books.append(
                    {"index": index, "book_id": book_id, "error": f"Book with ID '{book_id}' does not exist."}
                )
            
            # Validasi quantity
            if quantity <= 0:
                invalid_quantities.append(
                    {"index": index, "quantity": quantity, "error": "Quantity must be greater than 0."}
                )
        
        errors = {}
        if invalid_books:
            errors["invalid_books"] = invalid_books
        if invalid_quantities:
            errors["invalid_quantities"] = invalid_quantities
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return value
     
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
   
   
   
      
      

      
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

 

from django.db import models
from django.contrib.auth.models import AbstractUser  # Menggunakan User model default

#MODEL UNTUK TABEL User(1)
class User(AbstractUser):
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    
     # Override related_name to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Custom related name to avoid clash
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Custom related name to avoid clash
        blank=True,
    )
    
    def __str__(self):
        return self.username


#MODEL UNTUK TABEL BUKU(2)
class Book(models.Model):
   title = models.CharField(max_length=50)
   author = models.CharField(max_length=50)
   price = models.DecimalField(max_digits=10, decimal_places=2)
   stock = models.IntegerField()
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

# set nama tabel
   class Meta:
      db_table = 'books'
      
   def __str__(self):
      return self.title
   
   
#MODEL UNTUK TABEL TRANSAKSI(3)
class Transaction(models.Model):
   transaction_date = models.DateField(auto_now_add=True)
   total_amount = models.DecimalField(max_digits=10, decimal_places=2)
   
#SET RELASI KE TABEL CUSTOMER
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   
# set nama tabel
   class Meta:
      db_table = 'transactions'
      
   def __str__(self):
      return f"Transaction on {self.transaction_date} for {self.total_amount} (Customer: {self.user_id.username})"
 
# mengambil relasi ke TransactionItem untuk field items di serializer 
   @property
   def items(self):
      return self.transactionitem_set.all() 


#MODEL UNTUK TABEL TRANSACTION_ITEM(4)
class TransactionItem(models.Model):
   quantity = models.IntegerField()
   price_total = models.DecimalField(max_digits=10, decimal_places=2)
   
#SET RELASI KE TABEL TRANSACTION & BUKU
   transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
   book = models.ForeignKey(Book, on_delete=models.CASCADE)   
   
# set nama tabel
   class Meta:
      db_table = 'transaction_items'
      
   def __str__(self):
      return f"{self.book_id.title} (x{self.quantity})"



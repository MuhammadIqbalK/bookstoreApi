from django.db import models

#MODEL UNTUK TABEL BUKU(1)
class Book(models.Model):
   title = models.CharField(max_length=50)
   author = models.CharField(max_length=50)
   price = models.DecimalField(max_digits=10, decimal_places=2)
   stock = models.IntegerField
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

# set nama tabel
   class Meta:
      db_table = 'books'
      
   def __str__(self):
      return self.title


#MODEL UNTUK TABEL CUSTOMER(2)
class Customer(models.Model):
   name = models.CharField(max_length=50)
   phone = models.IntegerField(max_length=12)
   email = models.EmailField(max_length=100)

# set nama tabel
   class Meta:
      db_table = 'customers'
      
   def __str__(self):
      return self.name

   
#MODEL UNTUK TABEL TRANSAKSI(3)
class Transaction(models.Model):
   transaction_date = models.DateField(auto_now_add=True)
   total_amount = models.DecimalField(max_digits=10, decimal_places=2)
   
#SET RELASI KE TABEL CUSTOMER
   customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
   
# set nama tabel
   class Meta:
      db_table = 'transactions'
      
   def __str__(self):
      return f"Transaction on {self.transaction_date} for {self.total_amount} (Customer: {self.customer_id.name})"
   

#MODEL UNTUK TABEL TRANSACTION_ITEM(4)
class TransactionItem(models.Model):
   quantity = models.IntegerField
   price_total = models.DecimalField(max_digits=10, decimal_places=2)
   
#SET RELASI KE TABEL TRANSACTION & BUKU
   transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)
   book_id = models.ForeignKey(Book, on_delete=models.CASCADE)   
   
# set nama tabel
   class Meta:
      db_table = 'transaction_items'
      
   def __str__(self):
      return f"{self.book_id.title} (x{self.quantity})"



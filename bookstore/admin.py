from django.contrib import admin
from .models import Book
from django.utils import timezone



class BookAdmin(admin.ModelAdmin):
   #MENAMPILKAN SEMUA KOLOM BOOK
   list_display = ('title', 'author' ,'price' ,'stock' ,'created_at' ,'updated_at')
   #MENAMBAHKAN FITUR PENCARIAN BERDASARKAN 'TITLE' DAN 'AUTHOR'
   search_fields = ['title', 'author']
   #MENAMBAHKAN FILTER BERDASARKAN AUTHOR
   list_filter = ['author']
 
# MENGESET KOLOM "created_at" DENGAN TANGGAL&WAKTU SEKARANG  
def save_model(obj):
   obj.created_at = timezone.now()
   obj.save()

#MENDAFTARKAN BookAdmin KE HALAMAN ADMIN
admin.site.register(Book, BookAdmin)


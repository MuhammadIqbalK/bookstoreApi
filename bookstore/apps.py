from django.apps import AppConfig


class BookstoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookstore'
    
    def ready(self):
            # Memulai scheduler saat aplikasi dijalankan
            from .scheduler import start_scheduler
            import bookstore.signals
            start_scheduler()

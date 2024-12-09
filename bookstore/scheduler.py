from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from django.utils import timezone
from datetime import datetime
from .models import Transaction

# Fungsi yang akan memperbarui status transaction setiap 1 menit
def update_transaction_status():
    # Mengambil semua transaction dengan status 'pending' dan update status menjadi 'Late'
    transactions_to_update = Transaction.objects.filter(status='Pending')
    for transaction in transactions_to_update:
       if transaction.due_date < timezone.now():
            transaction.status = 'Late'
            transaction.save()
            print(f"transaction {transaction.id} status is updated to 'Late' in {datetime.now()}")

# Fungsi untuk memulai scheduler
def start_scheduler():
    scheduler = BackgroundScheduler()

    # Menjadwalkan fungsi update_transaction_status untuk dijalankan setiap 1 menit
    scheduler.add_job(update_transaction_status, 'interval', minutes=1)

    # Memulai scheduler
    scheduler.start()

    # Menangani event ketika pekerjaan selesai atau terjadi error
    def job_listener(event):
        if event.exception:
            print(f'Tasks failed executed: {event.job_id}')
        else:
            print(f'Tasks succesfully executed: {event.job_id}')

    # Menambahkan listener untuk mendengarkan event
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    return scheduler

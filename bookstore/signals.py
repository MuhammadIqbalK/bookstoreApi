from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # Membuat konteks untuk template email
    context = {
        'current_user': reset_password_token.user,  # Mengambil data user
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key
        )
    }

    # Menggunakan template email HTML
    email_html_message = render_to_string('password_reset_email.html', context)

    # Log untuk debugging
    print(f"Attempting to send email to: {reset_password_token.user.email}")
    print(f"Reset Password URL: {context['reset_password_url']}")
    # Mengirim email
    send_mail(
        # Subjek email
        "Password Reset for Your App Name",  # Ganti dengan nama aplikasi Anda
        '',  # Kosongkan body teks biasa karena kita akan menggunakan HTML
        'noreply@yourdomain.com',  # Ganti dengan email pengirim Anda
        [reset_password_token.user.email],  # Penerima email
        html_message=email_html_message,  # Body email HTML
        fail_silently=False,  # Tentukan apakah error harus ditangani
    )

    print("Email sent successfully")

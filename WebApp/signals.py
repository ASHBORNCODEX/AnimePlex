# WebApp/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from WebApp.models import RegistrationDB

@receiver(user_logged_in)
def set_session_after_google_login(sender, request, user, **kwargs):
    # Try to find a RegistrationDB record with this email
    reg_user, created = RegistrationDB.objects.get_or_create(
        E_Mail=user.email,
        defaults={'UserName': user.username, 'Password': '', 'C_Password': ''}
    )
    # Set session so existing pages work
    request.session['Name'] = reg_user.UserName

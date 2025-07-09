# auth/signals.py

from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import PhoneVerification
from django.contrib.auth.models import User

@receiver(post_delete, sender=PhoneVerification)
def delete_user_with_phone_verification(sender, instance, **kwargs):
    print(f'Deleting user with username: {instance.username}')
    try:
        user = User.objects.get(username=instance.username)
        user.delete()
    except User.DoesNotExist:
        pass

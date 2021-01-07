from .models import MessCont
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_mess(sender, instance, created, **kwargs):
    if created:
        MessCont.objects.create(user=instance)
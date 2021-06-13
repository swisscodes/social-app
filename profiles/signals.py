from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Person_profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_prolile_for_new_user(sender, created, instance, **kwarg):
    nickname = instance.email.rsplit("@", 1)[0].lower()
    if created:
        profile = Person_profile(user=instance, nickname=nickname)
        profile.save()

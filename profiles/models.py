from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save

# Create your models here.


class Person_profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_profile"
    )
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    nickname = models.CharField(max_length=30, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to="media/users/%Y/%m/%d", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=40, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address1 = models.CharField(blank=True, null=True, max_length=50)
    address2 = models.CharField(blank=True, null=True, max_length=50)
    phone = models.CharField(blank=True, null=True, max_length=25)
    zipcode = models.CharField(blank=True, null=True, max_length=10)

    class Meta:
        verbose_name = "Users profile"

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.user.email

    def get_profile(self):
        return self.pk

    def get_absolute_url(self):
        return reverse("add_later", kwargs={"pk": self.pk})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_prolile_for_new_user(sender, created, instance, **kwarg):
    if created:
        profile = Person_profile(user=instance)
        profile.save()

from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.


class Person_profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_profile"
    )
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    nickname = models.CharField(max_length=30, unique=True, null=False, blank=False)
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

    def get_full_name(self):
        is_un_named = self.first_name is None and self.last_name is None
        if is_un_named:
            return "Please set your first and last name in your profile"
        else:
            return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("add_later", kwargs={"pk": self.pk})

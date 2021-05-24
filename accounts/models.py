from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email is required to register")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"

    USERNAME_FIELD = "email"  # Here we are specifying the field to use for login
    # REQUIRED_FIELDS = ["email"]
    # we have to put this so it makes the email field required REQUIRED_FIELDS = ["username"]
    # else we will get required positional argument error

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Person_profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_profile"
    )
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d", blank=True, null=True)
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
        if self.username:
            return self.username
        else:
            return self.user.email

    def get_absolute_url(self):
        return reverse("add_later", kwargs={"pk": self.pk})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_prolile_for_new_user(sender, created, instance, **kwarg):
    if created:
        profile = Person_profile(user=instance)
        profile.save()

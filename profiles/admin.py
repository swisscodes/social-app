from django.contrib import admin
from .models import Person_profile


# Register your models here.
@admin.register(Person_profile)
class Person_profileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "nickname",
        "photo",
    )

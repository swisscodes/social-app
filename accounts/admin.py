from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User, Contact
from accounts.forms import CustomUserChangeForm, CustomUserCreationForm


# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("email", "is_active", "is_admin", "is_staff")
    list_filter = ("is_admin", "email")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        # ('Personal info', {'fields': ('date_of_birth',)}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "user_from",
        "user_to",
    )


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

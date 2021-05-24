# accounts/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms.widgets import DateInput, Input
from .models import User, Person_profile
from django.utils.html import format_html


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username or Email",
            },
        ),
    )
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "password", "is_active", "is_admin")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Person_profile
        fields = (
            "username",
            "first_name",
            "last_name",
            "date_of_birth",
            "country",
            "state",
            "city",
            "address1",
            "address2",
            "phone",
            "zipcode",
            "photo",
        )

        widgets = {
            "phone": Input(attrs={"type": "tel", "placeholder": "204873623"}),
            "date_of_birth": DateInput(attrs={"type": "date"}),
        }

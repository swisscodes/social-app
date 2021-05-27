from django import forms
from django.forms.widgets import DateInput, Input
from .models import Person_profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Person_profile
        fields = (
            "nickname",
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

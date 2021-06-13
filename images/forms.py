from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("title", "url", "description")

        # widgets = {"url": forms.HiddenInput}

        def clean_url(self):
            url = self.cleaned_data["url"]
            valid_extensions = ["jpg", "jpeg"]
            extension = url.rsplit(".", 1)[1].lower()
            # split from the first . from right split 1 only
            if extension not in valid_extensions:
                raise forms.ValidationError(
                    "The given URL does not " "match valid image extensions."
                )
            return url

        def save(self, force_insert=False, force_update=False, commit=True):
            image = super().save(commit=False)
            image_url = self.cleaned_data["url"]
            name = slugify(image.title)
            extension = image_url.rsplit(".", 1)[1].lower()
            image_name = f"{name}.{extension}"
            # download image from the given URL
            header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
            response = request.urlopen(image_url, header)
            image.image.save(image_name, ContentFile(response.read()), save=False)
            if commit:
                image.save()
            return image

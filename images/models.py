from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="user_images", on_delete=models.CASCADE
    )
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="images_liked", blank=True
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(blank=True)
    created = models.DateField(
        auto_now_add=True, db_index=True
    )  # Since you use auto_now_add, this datetime is automatically set when the object is created.

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "images:detail_view",
            args=[
                self.id,
                self.slug,
            ],
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # You use db_index=True so that Django creates an index in the database for this field.
    # Database indexes improve query performance. Consider setting db_index=True for fields that you frequently query using
    # filter(), exclude(), or order_by(). ForeignKey fields or fields with unique=True imply the creation of an index. You can
    # also use Meta.index_together or Meta.indexes to create

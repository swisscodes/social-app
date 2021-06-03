from django.urls import path
from .views import image_post_get, image_detail_view


app_name = "images"

urlpatterns = [
    path("", image_post_get, name="image_detail"),
    path("<slug:slug>/<int:img_pk>", image_post_get, name="image_details"),
    path("detail/<int:id>/<slug:slug>", image_detail_view, name="detail_view"),
]

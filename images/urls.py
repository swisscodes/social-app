from django.urls import path
from .views import (
    image_post_get,
    image_detail_view,
    image_like,
    image_list_view,
    image_ranking,
)


app_name = "images"

urlpatterns = [
    path("", image_list_view, name="list_view"),
    path("create/", image_post_get, name="image_detail"),
    path("<slug:slug>/<int:img_pk>", image_post_get, name="image_details"),
    path("detail/<int:id>/<slug:slug>", image_detail_view, name="detail_view"),
    path("like/", image_like, name="like"),
    path("ranking/", image_ranking, name="ranking"),
]

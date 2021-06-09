from django.urls import path
from .views import dashboard, edit_profile, user_list, user_detail, user_follow

app_name = "profiles"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("edit/", edit_profile, name="edit_profiles"),
    path("users/", user_list, name="user_list"),
    path("users/follow/", user_follow, name="user_follow"),
    path("users/<str:nickname>/", user_detail, name="user_detail"),
]

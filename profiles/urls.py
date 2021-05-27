from django.urls import path
from .views import dashboard, edit_profile

app_name = "profiles"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("edit", edit_profile, name="edit_profiles"),
]

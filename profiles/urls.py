from django.urls import path
from .views import dashboard

app_name = "profiles"

urlpatterns = [
    path("", dashboard, name="dashboard"),
]

from django.urls import path
from .views import action


app_name = "actions"

urlpatterns = [
    path("", action, name="action"),
]

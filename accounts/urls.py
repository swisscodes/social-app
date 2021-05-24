from django.urls import path
from .views import login_page, logout_page


app_name = "accounts"

urlpatterns = [
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),
]

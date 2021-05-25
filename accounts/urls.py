from django.contrib.auth import views as auth_views
from django.urls import path
from .views import login_page, logout_page


app_name = "accounts"

urlpatterns = [
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]

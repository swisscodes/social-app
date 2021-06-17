from django.contrib.auth import views as auth_views
from django.urls import path
from .views import login_page, logout_page, sign_up, google


app_name = "accounts"

urlpatterns = [
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),
    path("signup/", sign_up, name="signup"),
    path("google48bd223165802762.html/", google, name="google")
    # Django also provides the authentication URL patterns that you just created. You
    # can comment out the authentication URL patterns that you added to the urls.py
    # file of the account application and include django.contrib.auth.urls instead,
    # as follows:
    # from django.urls import path, include
    # # ...
    # urlpatterns = [
    # # ...
    # path('', include('django.contrib.auth.urls')),
    # ]
    # path(
    #     "password_change/",
    #     auth_views.PasswordChangeView.as_view(),
    #     name="password_change",
    # ),
    # path(
    #     "password_change/done/",
    #     auth_views.PasswordChangeDoneView.as_view(),
    #     name="password_change_done",
    # ),
    # path(
    #     "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    # ),
    # path(
    #     "password_reset/done/",
    #     auth_views.PasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "reset/<uidb64>/<token>/",
    #     auth_views.PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "reset/done/",
    #     auth_views.PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
]

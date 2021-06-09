from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from profiles.forms import ProfileForm
from .forms import LoginForm, CustomUserCreationForm
from actions.utils import create_action

# Create your views here.


def login_page(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            cd = form.cleaned_data
            user_field = None
            try:
                user_field = get_user_model().objects.get(
                    user_profile__nickname=cd["username"]
                )
            except get_user_model().DoesNotExist:
                try:
                    user_field = get_user_model().objects.get(email=cd["username"])
                except get_user_model().DoesNotExist:
                    pass
            if user_field:
                user = authenticate(
                    request, username=user_field.email, password=cd["password"]
                )
                if user:
                    if user.is_active:
                        login(request, user)
                        next = request.POST.get("next")
                        if next:
                            return redirect(next)
                        return redirect("home")
                    else:
                        return HttpResponse("Disabled account")
                else:
                    num_attempts = (request.session.get("attempts", 0)) + 1
                    request.session["attempts"] = num_attempts
                    messages.error(request, f"Incorrect password")
                    print(request.session["attempts"])
                    if num_attempts == 3:
                        request.session["attempts"] = 0
                        messages.error(
                            request, f"Incorrect password Your account is locked"
                        )
                        return render(
                            request, "registration/login.html", {"form": form}
                        )
                    return render(request, "registration/login.html", {"form": form})
            else:
                messages.error(request, "No user account found")
                return render(request, "registration/login.html", {"form": form})
    else:
        section = "login"
        context = {"form": form, "section": section}
        return render(request, "registration/login.html", context)


def sign_up(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == "POST":
        new_signed_up = CustomUserCreationForm(request.POST)
        if new_signed_up.is_valid():
            new_signed_up.save()
            create_action(new_signed_up, "has created an account")
            context = {"new_signed_up": new_signed_up}
            return render(request, "registration/register_done.html")
    section = "signup"
    context = {"form": form, "section": section}
    return render(request, "registration/register.html", context)


def profile_page(request, pk):
    if request.method == "POST":
        this_user = get_user_model().objects.get(pk=pk)
        if request.user == this_user:
            profile = ProfileForm(request.POST)
            if profile.is_valid():
                cd = profile.cleaned_data
                new_profile, created = ProfileForm.objects.update_or_create(
                    email=request.user,
                    defaults={
                        "photo": cd["photo"],
                        "date_of_birth": cd["date_of_birth"],
                        "country": cd["country"],
                        "state": cd["state"],
                        "city": cd["city"],
                        "address1": cd["address1"],
                        "address2": cd["address2"],
                        "phone": cd["phone"],
                        "zipcode": cd["zipcode"],
                    },
                )
                get_user_model().objects.filter(email=request.user).update(
                    username=cd["username"],
                    first_name=cd["first_name"],
                    last_name=cd["last_name"],
                )

    return render(request, "account/profile.html", {"ProfileForm": ProfileForm})


def home_page(request):
    return render(request, "home.html")


def logout_page(request):
    logged_user = request.user
    context = {"logged_user": logged_user}
    logout(request)
    return render(request, "registration/logout.html", context)

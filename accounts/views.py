from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import ProfileForm, LoginForm
from .models import User

# Create your views here.


def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_field = None
            try:
                user_field = User.objects.get(user_profile__username=cd["username"])
            except User.DoesNotExist:
                try:
                    user_field = User.objects.get(email=cd["username"])
                except User.DoesNotExist:
                    pass
            if user_field:
                user = authenticate(
                    request, username=user_field.email, password=cd["password"]
                )
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        print(request.session.__dict__)
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
                messages.error(
                    request, "Please check your username and or Email is correct"
                )
                return render(request, "registration/login.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, "registration/login.html", {"form": form})


def profile_page(request, pk):
    if request.method == "POST":
        this_user = User.objects.get(pk=pk)
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
                User.objects.filter(email=request.user).update(
                    username=cd["username"],
                    first_name=cd["first_name"],
                    last_name=cd["last_name"],
                )

    return render(request, "account/profile.html", {"ProfileForm": ProfileForm})


def home_page(request):
    return render(request, "home.html")


def logout_page(request):
    return render(request, "registration/logout.html")

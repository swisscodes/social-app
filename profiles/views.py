from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm

# Create your views here.


@login_required
def dashboard(request):
    context = {"section": "dashboard"}
    return render(request, "profiles/dashboard.html", context)


@login_required
def edit_profile(request):
    form = ProfileForm(
        request.POST or None, request.FILES or None, instance=request.user.user_profile
    )
    if request.method == "POST":
        if form.is_valid():
            form.save()
            if request.POST.get("save") == "save":
                messages.success(request, "Profile updated " "successfully")
                return redirect("profiles:dashboard")
            messages.success(request, "Cancelled " "successfully")
            return redirect("profiles:dashboard")
        else:
            messages.error(request, f"Error updating your profile")
    context = {
        "form": form,
    }
    return render(request, "profiles/edit_profiles.html", context)

from actions.utils import create_action
from django.http.response import HttpResponse
from accounts.models import User
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .forms import ProfileForm
from django.http import JsonResponse
from images.models import Contact
from common.decorators import ajax_required


# Create your views here.


@login_required
def dashboard(request):
    current_user_images = request.user.user_images.all().order_by("-created")
    paginator = Paginator(current_user_images, 10)
    page = request.GET.get("page")
    try:
        current_user_images = paginator.page(page)
    except PageNotAnInteger:
        current_user_images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse("")
        current_user_images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        context = {"section": "images", "current_user_images": current_user_images}
        return render(
            request,
            "profiles/list_ajax.html",
            context,
        )
    context = {
        "section": "dashboard",
        "current_user_images": current_user_images,
        "paginator": paginator,
    }
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


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    users = users.select_related("user_profile")
    context = {"section": "people", "users": users}
    return render(request, "profiles/user_list.html", context)


@login_required
def user_detail(request, nickname):
    try:
        this_user = (
            User.objects.select_related("user_profile")
            .prefetch_related("rel_to")
            .get(user_profile__nickname=nickname, is_active=True)
        )
    except User.DoesNotExist:
        return HttpResponse("Page does not exist")
    if request.user in this_user.rel_to.all():
        following = True
        print("Following you", following)
    else:
        following = False
        print("following you", following)
    context = {
        "section": "people",
        "this_user": this_user,
        "in_or_out": following,
    }
    return render(request, "profiles/user_detail.html", context)


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            this_user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=this_user)
                create_action(request.user, "is following", this_user)
            else:
                Contact.objects.filter(
                    user_from=request.user, user_to=this_user
                ).delete()
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error"})
    return JsonResponse({"status": "error"})

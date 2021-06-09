from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import ImageForm
from .models import Image
from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action

# Create your views here.


@login_required
def image_list_view(request):
    all_images = Image.objects.all().order_by("-created")
    paginator = Paginator(all_images, 10)
    page = request.GET.get("page")

    try:
        all_images = paginator.page(page)
    except PageNotAnInteger:
        all_images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse("")
        all_images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        context = {"section": "images", "all_images": all_images}
        return render(
            request,
            "images/list_ajax.html",
            context,
        )
    context = {"section": "images", "all_images": all_images}
    return render(request, "images/list.html", context)


@login_required
def image_post_get(request):
    if request.method == "POST":
        form = ImageForm(
            data=request.POST,
        )
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, "bookmarked image", new_item)
            section = "images"
            context = {
                "form": form,
                "section": section,
            }
            messages.success(request, "Image added successfully")
            return redirect(new_item.get_absolute_url())
    form = ImageForm(data=request.GET)
    section = "images"
    context = {
        "form": form,
        "section": section,
    }
    return render(request, "images/images.html", context)


@login_required
def image_detail_view(request, id, slug):
    try:
        this_image = Image.objects.get(id=id, slug=slug)
    except Image.DoesNotExist:
        return HttpResponse("Page does not exist")
    context = {
        "this_image": this_image,
        "section": "images",
    }
    return render(request, "images/image_detail_view.html", context)


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        print(action)
        try:
            this_image = Image.objects.get(id=image_id)
            if action == "like":
                this_image.users_like.add(request.user)
                create_action(request.user, "likes", this_image)
            else:
                this_image.users_like.remove(request.user)
                create_action(request.user, "Unlikes", this_image)
            return JsonResponse({"status": "ok"})
        except:
            pass
    return JsonResponse({"status": "error"})

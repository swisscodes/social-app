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
from django.conf import settings
import redis


r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


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
def image_post_get(request, obj_instance=None):
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
    if request.is_ajax() and "action" in request.POST:
        obj = request.POST.get("obj")
        action = request.POST.get("action")
        if action == "edit":
            form = ImageForm(data=request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({"status": "saved"})
    if obj_instance:
        obj = request.user.user_images.get(id=obj_instance)
        form = ImageForm(instance=obj)
        context = {
            "form": form,
            "section": "images",
        }
        return render(request, "images/images.html", context)

    form = ImageForm(data=request.GET)
    context = {
        "form": form,
        "section": "images",
    }
    return render(request, "images/images.html", context)


@login_required
def image_detail_view(request, id, slug):
    try:
        this_image = Image.objects.get(id=id, slug=slug)
    except Image.DoesNotExist:
        return HttpResponse("Page does not exist")
    total_views = r.incr(f"image:{this_image.id}:views", 0)
    user_just_viewed = r.sadd(f"{this_image.id}", f"{request.user.id}")
    if user_just_viewed:
        # increment total image views by 1
        total_views = r.incr(f"image:{this_image.id}:views", 1)
        # increment image ranking by 1
        # name of set, increamentby, objects of set
        r.zincrby("image_ranking", 1, this_image.id)
    context = {
        "this_image": this_image,
        "section": "images",
        "total_views": total_views,
    }
    return render(request, "images/image_detail_view.html", context)


@login_required
def image_ranking(request):
    # get image ranking dictionary
    # the the_set, 0 starts from lowest, -1 to the last, desc=True descending order
    image_ranking = r.zrange("image_ranking", 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    context = {"section": "images", "most_viewed": most_viewed}
    return render(request, "images/ranking.html", context)


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
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

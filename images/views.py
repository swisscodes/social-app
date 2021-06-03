from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import ImageForm
from .models import Image
from django.urls import reverse

# Create your views here.


@login_required
def image_post_get(request):
    if request.method == "POST":
        form = ImageForm(
            data=request.POST,
        )
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            section = "images"
            context = {
                "form": form,
                "section": section,
            }
            return redirect(new_item.get_absolute_url())
    form = ImageForm(
        data=request.GET,
    )
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

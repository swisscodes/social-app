from django.shortcuts import render


def home_page(request):
    context = {"section": "home"}
    return render(request, "home.html", context)

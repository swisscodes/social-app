from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def dashboard(request):
    context = {"section": "dashboard"}
    return render(request, "profiles/dashboard.html", context)

from actions.models import Action
from django.shortcuts import render


def home_page(request):
    actions = None
    if request.user.is_authenticated:
        following_ids = request.user.following.values_list("id", flat=True)
        if following_ids:
            actions = Action.objects.filter(user__in=following_ids).exclude(
                user=request.user
            )
            # If user is following others, retrieve only their actions
            actions = actions.select_related("user", "user__user_profile")[
                :10
            ].prefetch_related("target", "user__user_images")[:10]
            context = {"section": "home", "actions": actions}
            return render(request, "home.html", context)
    context = {"section": "home", "actions": actions}
    return render(request, "home.html", context)


def google(request):
    return render(request, "google.html")

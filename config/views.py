from actions.models import Action
from django.shortcuts import render


def home_page(request):
    actions = None
    if request.user.is_authenticated:
        actions = Action.objects.exclude(user=request.user)
        following_ids = request.user.rel_from.values_list("id", flat=True)
        if following_ids:
            # If user is following others, retrieve only their actions
            actions = actions.select_related("user", "user__user_profile")[
                :10
            ].prefetch_related("target")[:10]
        context = {"section": "home", "actions": actions}
        return render(request, "home.html", context)
    context = {"section": "home", "actions": actions}
    return render(request, "home.html", context)

from django import template


register = template.Library()


@register.simple_tag(name="follows_you")
def follows_you(request):
    yes_no = request.user.rel_to.all()
    return yes_no

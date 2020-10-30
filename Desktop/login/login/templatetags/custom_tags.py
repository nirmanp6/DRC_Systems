 from django import template
  register = template.Library()

  from products.models import cart

@register.simple_tag
def cart_dynamic(request):
    qs = cart.objects.filter(user__email = request.user.email)
    if qs.exists():
        return cart.quantity

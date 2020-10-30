from django import template
register = template.Library()

from products.models import cart

@register.simple_tag
def cart_dynamic(user):
    user = user
    qs = cart.objects.filter(user__email = user.email,status="1")
    if qs.exists():
        cart1 = qs[0]
        return cart1.quantity

    else:
    	return 0

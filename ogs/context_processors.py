from .models import Cart, CartItem

def cart_count(request):

    count = 0

    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(user=request.user)

        count = CartItem.objects.filter(cart=cart).count()

    return {
        'cart_count': count
    }
from django.shortcuts import render, redirect, get_object_or_404
from ecom_app.models import products
from.models import cart,cartitem
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    Cart=request.session.session_key
    if not Cart:
        Cart = request.session.create()

    return Cart

def add_cart(request,product_id):
    product=products.objects.get(id=product_id)
    try:
        Cart=cart.objects.get(cart_id=_cart_id(request))
    except cart.DoesNotExist:
        Cart=cart.objects.create(cart_id=_cart_id(request))
        Cart.save()
    try:
        cart_item=cartitem.objects.get(product=product,cart=Cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity+=1
        cart_item.save()
    except cartitem.DoesNotExist:
        cart_item=cartitem.objects.create(product=product,quantity=1,cart=Cart)
        cart_item.save()

    return redirect('cart:cart_detail')

def cart_detail(request,total=0, counter=0,cart_items=None):
    try:
        Cart=cart.objects.get(cart_id=_cart_id(request))
        cart_items=cartitem.objects.filter(cart=Cart,active=True)
        for cart_item in cart_items:
            total += (cart_item.product.prize * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter))

def cart_remove(request,product_id):
    Cart=cart.objects.get(cart_id=_cart_id(request))
    produt=get_object_or_404(products,id=product_id)
    cart_item=cartitem.objects.get(product=produt,cart=Cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')
def full_remove(request,product_id):
    Cart = cart.objects.get(cart_id=_cart_id(request))
    produt = get_object_or_404(products, id=product_id)
    cart_item = cartitem.objects.get(product=produt, cart=Cart)
    cart_item.delete()
    return redirect('cart:cart_detail')


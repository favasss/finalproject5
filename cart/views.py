from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from cart.models import Cart, CartItem
from finalapp5.models import Movie


# Create your views here.
def _cart_id(request):
    cart=request.session.session_key

    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,movie_id):
    movie=Movie.objects.get(id=movie_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
                 cart_id=_cart_id(request)
        )
        cart.save()
    try:
        cart_item = CartItem.objects.get(movie=movie, cart=cart)
        # If the movie is already in the cart, print a message and return
        messages.info(request, f"{movie.name} already satisfied.")
        return redirect('cart:cart_detail')
    except CartItem.DoesNotExist:
        # If the movie is not in the cart, create a new CartItem
        cart_item = CartItem.objects.create(
            movie=movie,
            quantity=1,
            cart=cart
        )
        messages.success(request, f"{movie.name} added to cart.")
    return redirect('cart:cart_detail')
def cart_detail(request,total=0,counter=0,cart_items=None):

    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart.id,active=True)
        print(cart_items)
        for cart_item in cart_items:

            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter))

def full_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    movie=get_object_or_404(Movie,id=product_id)
    cart_item=CartItem.objects.get(movie=movie,cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')


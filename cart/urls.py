from django.urls import path
from . import views


app_name='cart'

urlpatterns = [
    path('',views.cart_detail,name='cart_detail'),
    path('add/<int:movie_id>/',views.add_cart,name='add_cart'),
    path('full_remove/<int:product_id>/',views.full_remove,name='full_remove')

    ]

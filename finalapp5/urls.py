from django.urls import path
from finalapp5 import views
app_name='finalapp5'
urlpatterns = [
    path('',views.register,name='register'),
    path('login.html',views.login,name='login'),
    path('allProdCat/',views.allProdCat,name='allProdCat'),
    path('<slug:c_slug>/',views.allProdCat,name='products_by_category'),
    path('<slug:c_slug>/<slug:movie_slug>/',views.proDetail,name='prodCatdetail'),
    path('browse', views.browse, name='browse'),
    path('finalapp5/edit/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('finalapp5/delete/<int:movie_id>/',views.delete_movie, name='delete_movie'),
    path('profile', views.profile, name='profile'),
    path('finalapp5/<int:movie_id>/add_review/',views.add_review, name='add_review'),
    path('logout',views.logout,name='logout')
]

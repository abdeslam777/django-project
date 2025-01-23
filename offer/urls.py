from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
        path('home/' , views.home , name='home'),
        path('',  views.offer , name='offer'),
        path('offer_list/',  views.offer_list , name='offer_list'),
        path('offer/<int:pk>/' , views.offer_detail,name='offer_detail'),
        path('offer/<int:pk>/apply/', views.apply_offer, name='apply_offer'),
        path('create-offer/' , views.create_offer , name='create-offer'),
        path('update-offer/<int:pk>/' , views.update_offer , name='update-offer'),
        path('delete-offer/<int:pk>/' , views.delete_offer , name='delete-offer'),
        path('applications/', views.application_list, name='application_list'),
        # path('applications/<int:offer_id>/', views.application_list, name='offer_applications'),
        path('login/', views.loginPage , name='login'),
        path('logout/', views.logoutUser, name='logout'),
        path('register/', views.registerPage, name='register'),
        # path('add-to-watchlist/<int:offer_id>/', views.add_to_watchlist, name='add_to_watchlist'),
        # path('remove-from-watchlist/<int:watchlist_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
        # path('watchlist/', views.view_watchlist, name='view_watchlist'),
]
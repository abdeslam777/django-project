from django.urls import path
from . import views

urlpatterns = [

    path('profile/', views.user_profile ,name='user-profile'),
    # path('supervisor/<int:supervisor_id>/', views.supervisor_profile, name='supervisor-profile'),
]
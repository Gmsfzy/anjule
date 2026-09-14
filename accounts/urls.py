from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user-login'),
    path('register/', views.user_register, name='user-register'),
    path('logout/', views.user_logout, name='user-logout'),
    path('profile/', views.user_profile, name='user-profile'),
    path('super/users/', views.super_user_list, name='super-users-list'),
    path('property/users/', views.property_user_list, name='property-users-list'),
]
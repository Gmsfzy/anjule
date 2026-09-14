from django.urls import path
from . import views

urlpatterns = [
    path('communities/', views.community_list, name='communities-list'),
    path('buildings/', views.building_list, name='buildings-list'),
    path('houses/', views.house_list, name='houses-list'),
    path('resident/houses/', views.resident_house_list, name='resident-houses-list'),
]
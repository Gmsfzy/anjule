from django.urls import path, include
from . import views

from .views import HouseListView

urlpatterns = [
    path('repair-orders/', views.repair_order_list, name='repair-orders-list'),
    path('notices/', views.notice_list, name='notices-list'),
    path('payments/', views.payment_list, name='payments-list'),
    path('', HouseListView.as_view(), name='house_list'),
]
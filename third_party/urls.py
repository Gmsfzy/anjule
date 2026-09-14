from django.urls import path
from . import views

urlpatterns = [
    # 支付接口页面
    path('payment/', views.payment_page, name='third_party_payment'),
    # 门禁接口页面
    path('access/', views.access_page, name='third_party_access'),
]   
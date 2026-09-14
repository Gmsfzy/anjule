from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import RepairOrderViewSet, NoticeViewSet, PaymentRecordViewSet



router = DefaultRouter()
# 给每个ViewSet手动指定basename（见名知意，和路由前缀对应）
router.register(r'repair-orders', RepairOrderViewSet, basename='repair-order')
router.register(r'notices', NoticeViewSet, basename='notice')
router.register(r'payments', PaymentRecordViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),

]
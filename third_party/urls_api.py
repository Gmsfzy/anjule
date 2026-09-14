from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_api

# 初始化DRF路由器
router = DefaultRouter()
# 注册第三方支付ViewSet（加basename避免AssertionError）
router.register(r'payment', views_api.PaymentApiViewSet, basename='third-party-payment')
# 注册第三方门禁ViewSet（加basename避免AssertionError）
router.register(r'access', views_api.AccessApiViewSet, basename='third-party-access')

# API路由配置
urlpatterns = [
    path('', include(router.urls)),
]
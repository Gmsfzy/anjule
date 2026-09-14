from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import (
    UserRegisterView, UserLoginView, SuperAdminUserViewSet,
    PropertyUserViewSet, ResidentProfileView
)

router = DefaultRouter()
router.register(r'super/users', SuperAdminUserViewSet, basename='super_user')
router.register(r'property/users', PropertyUserViewSet, basename='property_user')

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='api-user-register'),
    path('login/', UserLoginView.as_view(), name='api-user-login'),
    path('resident/profile/', ResidentProfileView.as_view(), name='api-resident-profile'),
    path('', include(router.urls)),
]
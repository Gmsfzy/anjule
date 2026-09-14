from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_api  # 确保导入了对应的ViewSet

router = DefaultRouter()
# 给所有无queryset的ViewSet手动指定basename（值自定义，见名知意即可）
router.register(r'communities', views_api.CommunityViewSet, basename='community')
router.register(r'buildings', views_api.BuildingViewSet, basename='building')
router.register(r'houses', views_api.HouseViewSet, basename='house')
router.register(r'resident/houses', views_api.ResidentHouseViewSet, basename='resident-houses')

# 最终urlpatterns（如果有的话）
urlpatterns = [
    path('', include(router.urls)),
]
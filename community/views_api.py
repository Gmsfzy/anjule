from rest_framework import viewsets
from .models import Community, Building, House
from .serializers import CommunitySerializer, BuildingSerializer, HouseSerializer
from accounts.permissions import IsSuperAdmin, IsPropertyOrSuperAdmin, IsResident

# 小区管理（超级管理员）
class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsSuperAdmin]

# 楼栋管理（物业/超级管理员）
class BuildingViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingSerializer
    permission_classes = [IsPropertyOrSuperAdmin]

    def get_queryset(self):
        if self.request.user.role == 'property_admin':
            return Building.objects.filter(community=self.request.user.community)
        return Building.objects.all()

# 房屋管理（物业/超级管理员）
class HouseViewSet(viewsets.ModelViewSet):
    serializer_class = HouseSerializer
    permission_classes = [IsPropertyOrSuperAdmin]

    def get_queryset(self):
        if self.request.user.role == 'property_admin':
            return House.objects.filter(building__community=self.request.user.community)
        return House.objects.all()

# 住户查看自己的房屋信息
class ResidentHouseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HouseSerializer
    permission_classes = [IsResident]

    def get_queryset(self):
        return House.objects.filter(owner=self.request.user)
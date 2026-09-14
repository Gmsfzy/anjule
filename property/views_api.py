from rest_framework import viewsets, filters
from .models import RepairOrder, Notice, PaymentRecord
from .serializers import RepairOrderSerializer, NoticeSerializer, PaymentRecordSerializer
from accounts.permissions import IsSuperAdmin, IsPropertyAdmin, IsResident, IsPropertyOrSuperAdmin





# 报修单管理
class RepairOrderViewSet(viewsets.ModelViewSet):
    serializer_class = RepairOrderSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['create_time', 'status']

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsResident]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsPropertyAdmin]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsPropertyOrSuperAdmin | IsResident]
        else:
            permission_classes = [IsSuperAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'resident':
            return RepairOrder.objects.filter(reporter=user)
        elif user.role == 'property_admin':
            return RepairOrder.objects.filter(house__building__community=user.community)
        return RepairOrder.objects.all()

# 公告管理
class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsPropertyOrSuperAdmin]
        else:
            permission_classes = [IsResident | IsPropertyOrSuperAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'resident':
            return Notice.objects.filter(community=user.community)
        elif user.role == 'property_admin':
            return Notice.objects.filter(community=user.community)
        return Notice.objects.all()

# 缴费记录管理
class PaymentRecordViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentRecordSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsPropertyOrSuperAdmin]
        else:
            permission_classes = [IsResident | IsPropertyOrSuperAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'resident':
            return PaymentRecord.objects.filter(house__owner=user)
        elif user.role == 'property_admin':
            return PaymentRecord.objects.filter(house__building__community=user.community)
        return PaymentRecord.objects.all()

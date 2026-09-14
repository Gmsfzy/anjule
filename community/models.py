from django.db import models
from accounts.models import User
from django.utils import timezone


# 小区模型
class Community(models.Model):
    name = models.CharField(max_length=100, verbose_name='小区名称')
    address = models.CharField(max_length=200, verbose_name='小区地址')
    developer = models.CharField(max_length=100, blank=True, null=True, verbose_name='开发商')
    property_company = models.CharField(max_length=100, blank=True, null=True, verbose_name='物业公司')
    build_time = models.DateField(blank=True, null=True, verbose_name='建成时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,  # 之前加的空值，解决循环依赖
        related_name='managed_communities',  # 核心：避免和User的community字段冲突
        verbose_name='小区管理员'
    )

    class Meta:
        verbose_name = '小区'
        verbose_name_plural = '小区'

    def __str__(self):
        return self.name

# 楼栋模型
class Building(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name='所属小区')
    name = models.CharField(max_length=50, verbose_name='楼栋名称')
    unit_count = models.IntegerField(default=1, verbose_name='单元数')
    floor_count = models.IntegerField(default=18, verbose_name='楼层数')

    class Meta:
        verbose_name = '楼栋'
        verbose_name_plural = '楼栋'

    def __str__(self):
        return f'{self.community.name} - {self.name}'

# 房屋模型
class House(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name='所属楼栋')
    unit = models.IntegerField(verbose_name='单元号')
    floor = models.IntegerField(verbose_name='楼层')
    room_number = models.CharField(max_length=10, verbose_name='房间号')
    area = models.FloatField(verbose_name='房屋面积')
    owner = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='房屋业主'
    )
    is_rented = models.BooleanField(default=False, verbose_name='是否出租')

    class Meta:
        verbose_name = '房屋'
        verbose_name_plural = '房屋'
        unique_together = ('building', 'unit', 'floor', 'room_number')

    def __str__(self):
        return f'{self.building.name} {self.unit}单元{self.floor}层{self.room_number}室'
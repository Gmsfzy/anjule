from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# 角色枚举
class Role(models.TextChoices):
    SUPER_ADMIN = 'super_admin', _('超级管理员')
    PROPERTY_ADMIN = 'property_admin', _('物业管理员')
    RESIDENT = 'resident', _('小区住户')
    THIRD_PARTY = 'third_party', _('第三方服务商')

# 自定义用户模型
class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.RESIDENT,
        verbose_name='用户角色'
    )
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号')
    id_card = models.CharField(max_length=18, blank=True, null=True, verbose_name='身份证号')
    community = models.ForeignKey(
        'community.Community',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='所属小区'
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
from django.db import models
from accounts.models import User
from community.models import Community, House

# 报修单模型
class RepairOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )

    title = models.CharField(max_length=100, verbose_name='报修标题')
    content = models.TextField(verbose_name='报修内容')
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='报修房屋')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repair_reporter', verbose_name='报修人')
    handler = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_handler',
        verbose_name='处理人'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    completion_note = models.TextField(blank=True, null=True, verbose_name='完成备注')

    class Meta:
        verbose_name = '报修单'
        verbose_name_plural = '报修单'

    def __str__(self):
        return f'{self.title} ({self.get_status_display()})'

# 小区公告模型
class Notice(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name='所属小区')
    title = models.CharField(max_length=100, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发布人')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')

    class Meta:
        verbose_name = '小区公告'
        verbose_name_plural = '小区公告'
        ordering = ['-is_top', '-publish_time']

    def __str__(self):
        return f'{self.community.name} - {self.title}'

# 缴费记录模型
class PaymentRecord(models.Model):
    PAYMENT_TYPE = (
        ('property_fee', '物业费'),
        ('water_fee', '水费'),
        ('electric_fee', '电费'),
        ('gas_fee', '燃气费'),
        ('parking_fee', '停车费'),
        ('other', '其他费用'),
    )

    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='缴费房屋')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE, verbose_name='缴费类型')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='缴费金额')
    payer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='缴费人')
    payment_time = models.DateTimeField(auto_now_add=True, verbose_name='缴费时间')
    payment_method = models.CharField(max_length=20, blank=True, null=True, verbose_name='缴费方式')
    third_party_order_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='第三方订单号')

    class Meta:
        verbose_name = '缴费记录'
        verbose_name_plural = '缴费记录'

    def __str__(self):
        return f'{self.house} - {self.get_payment_type_display()} - {self.amount}元'
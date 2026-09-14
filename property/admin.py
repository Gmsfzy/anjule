from django.contrib import admin
from .models import RepairOrder, Notice, PaymentRecord

@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'house', 'reporter', 'status', 'create_time')
    list_filter = ('status', 'create_time', 'house__building__community')
    search_fields = ('title', 'content', 'reporter__username')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'community', 'publisher', 'is_top', 'publish_time')
    list_filter = ('is_top', 'publish_time', 'community')
    search_fields = ('title', 'content')

@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('house', 'payment_type', 'amount', 'payer', 'payment_time')
    list_filter = ('payment_type', 'payment_time', 'house__building__community')
    search_fields = ('house__room_number', 'payer__username')
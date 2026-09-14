from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'get_role_display', 'phone', 'community', 'is_active')
    list_filter = ('role', 'community', 'is_active')
    search_fields = ('username', 'phone', 'email')
    fieldsets = (
        ('基本信息', {'fields': ('username', 'password', 'email', 'phone', 'id_card')}),
        ('权限配置', {'fields': ('role', 'community', 'is_active', 'is_staff', 'is_superuser')}),
        ('时间信息', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined')
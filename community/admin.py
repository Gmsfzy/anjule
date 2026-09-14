from django.contrib import admin
from .models import Community, Building, House

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'property_company', 'build_time')
    search_fields = ('name', 'address', 'property_company')

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'community', 'unit_count', 'floor_count')
    list_filter = ('community',)
    search_fields = ('name',)

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'building', 'area', 'owner', 'is_rented')
    list_filter = ('building__community', 'is_rented')
    search_fields = ('room_number', 'owner__username')
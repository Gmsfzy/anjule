from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Community, Building, House
from accounts.permissions import IsSuperAdmin, IsPropertyAdmin


# 超级管理员 - 小区管理
@login_required
def community_list(request):
    if request.user.role != 'super_admin':
        messages.error(request, '无权限访问')
        return redirect('index')

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        developer = request.POST.get('developer')
        property_company = request.POST.get('property_company')
        Community.objects.create(
            name=name,
            address=address,
            developer=developer,
            property_company=property_company
        )
        messages.success(request, '小区创建成功')
        return redirect('communities-list')

    communities = Community.objects.all()
    return render(request, 'community/community_list.html', {'communities': communities})


# 楼栋管理
@login_required
def building_list(request):
    if request.user.role not in ['super_admin', 'property_admin']:
        messages.error(request, '无权限访问')
        return redirect('index')

    # 筛选小区
    if request.user.role == 'property_admin':
        communities = [request.user.community]
        buildings = Building.objects.filter(community=request.user.community)
    else:
        communities = Community.objects.all()
        buildings = Building.objects.all()

    if request.method == 'POST':
        community_id = request.POST.get('community')
        name = request.POST.get('name')
        unit_count = request.POST.get('unit_count', 1)
        floor_count = request.POST.get('floor_count', 18)

        community = get_object_or_404(Community, id=community_id)
        Building.objects.create(
            community=community,
            name=name,
            unit_count=unit_count,
            floor_count=floor_count
        )
        messages.success(request, '楼栋创建成功')
        return redirect('buildings-list')

    return render(request, 'community/building_list.html', {
        'communities': communities,
        'buildings': buildings
    })


# 房屋管理
@login_required
def house_list(request):
    if request.user.role not in ['super_admin', 'property_admin']:
        messages.error(request, '无权限访问')
        return redirect('index')

    # 筛选楼栋
    if request.user.role == 'property_admin':
        buildings = Building.objects.filter(community=request.user.community)
    else:
        buildings = Building.objects.all()

    # 住户列表（绑定房屋用）
    from accounts.models import User
    residents = User.objects.filter(role='resident')

    if request.method == 'POST':
        building_id = request.POST.get('building')
        unit = request.POST.get('unit')
        floor = request.POST.get('floor')
        room_number = request.POST.get('room_number')
        area = request.POST.get('area')
        owner_id = request.POST.get('owner')
        is_rented = request.POST.get('is_rented') == 'on'

        building = get_object_or_404(Building, id=building_id)
        owner = get_object_or_404(User, id=owner_id) if owner_id else None

        House.objects.create(
            building=building,
            unit=unit,
            floor=floor,
            room_number=room_number,
            area=area,
            owner=owner,
            is_rented=is_rented
        )
        messages.success(request, '房屋创建成功')
        return redirect('houses-list')

    # 房屋列表
    if request.user.role == 'property_admin':
        houses = House.objects.filter(building__community=request.user.community)
    else:
        houses = House.objects.all()

    return render(request, 'community/house_list.html', {
        'buildings': buildings,
        'residents': residents,
        'houses': houses
    })


# 住户查看自己的房屋
@login_required
def resident_house_list(request):
    if request.user.role != 'resident':
        messages.error(request, '无权限访问')
        return redirect('index')

    houses = House.objects.filter(owner=request.user)
    return render(request, 'community/resident_house_list.html', {'houses': houses})
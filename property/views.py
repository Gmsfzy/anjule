from contextvars import Token

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import RepairOrder, Notice, PaymentRecord
from community.models import House, Community
from accounts.models import User

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny  # 导入允许匿名访问的权限类


class HouseListView(APIView):
    permission_classes = [AllowAny]  # 单独设置该接口允许匿名访问（仅调试用）



    # 处理GET请求
    def get(self, request, *args, **kwargs):
        # 测试数据（格式与Flutter端的HouseModel对应）
        test_houses = [
            {"id": 1, "name": "三室一厅精装房", "price": 1200000, "address": "北京市朝阳区建国路88号"},
            {"id": 2, "name": "两室一厅简装房", "price": 800000, "address": "上海市浦东新区张江路150号"},
            {"id": 3, "name": "单身公寓", "price": 450000, "address": "广州市天河区天河路385号"}
        ]

        # 返回响应数据，与Flutter端对接
        return Response(
            data=test_houses,
            status=status.HTTP_200_OK
        )



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })




# 报修单管理
@login_required
def repair_order_list(request):
    # 不同角色查看不同报修单
    if request.user.role == 'resident':
        repair_orders = RepairOrder.objects.filter(reporter=request.user)
        houses = House.objects.filter(owner=request.user)
    elif request.user.role == 'property_admin':
        repair_orders = RepairOrder.objects.filter(house__building__community=request.user.community)
        handlers = User.objects.filter(role='property_admin', community=request.user.community)
    else:
        repair_orders = RepairOrder.objects.all()
        handlers = User.objects.filter(role='property_admin')

    # 提交报修单（住户）
    if request.method == 'POST' and request.user.role == 'resident':
        title = request.POST.get('title')
        content = request.POST.get('content')
        house_id = request.POST.get('house')

        house = get_object_or_404(House, id=house_id)
        RepairOrder.objects.create(
            title=title,
            content=content,
            house=house,
            reporter=request.user
        )
        messages.success(request, '报修单提交成功')
        return redirect('repair-orders-list')

    # 更新报修单状态（物业）
    if request.method == 'POST' and request.user.role == 'property_admin':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        handler_id = request.POST.get('handler')
        completion_note = request.POST.get('completion_note')

        order = get_object_or_404(RepairOrder, id=order_id)
        order.status = status
        order.handler = get_object_or_404(User, id=handler_id) if handler_id else None
        if status == 'completed':
            order.completion_note = completion_note
        order.save()
        messages.success(request, '报修单状态更新成功')
        return redirect('repair-orders-list')

    context = {'repair_orders': repair_orders}
    if request.user.role == 'resident':
        context['houses'] = houses
    if request.user.role == 'property_admin':
        context['handlers'] = handlers

    return render(request, 'property/repair_order_list.html', context)


# 公告管理
@login_required
def notice_list(request):
    # 不同角色查看不同公告
    if request.user.role == 'resident':
        notices = Notice.objects.filter(community=request.user.community)
    elif request.user.role == 'property_admin':
        notices = Notice.objects.filter(community=request.user.community)
    else:
        notices = Notice.objects.all()

    # 发布公告（物业/超级管理员）
    if request.method == 'POST' and request.user.role in ['property_admin', 'super_admin']:
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_top = request.POST.get('is_top') == 'on'
        community_id = request.POST.get('community')

        # 物业只能发布本小区公告
        if request.user.role == 'property_admin':
            community = request.user.community
        else:
            community = get_object_or_404(Community, id=community_id)

        Notice.objects.create(
            title=title,
            content=content,
            community=community,
            publisher=request.user,
            is_top=is_top
        )
        messages.success(request, '公告发布成功')
        return redirect('notices-list')

    context = {'notices': notices}
    if request.user.role == 'super_admin':
        context['communities'] = Community.objects.all()

    return render(request, 'property/notice_list.html', context)


# 缴费记录管理
@login_required
def payment_list(request):
    # 不同角色查看不同缴费记录
    if request.user.role == 'resident':
        payments = PaymentRecord.objects.filter(house__owner=request.user)
    elif request.user.role == 'property_admin':
        payments = PaymentRecord.objects.filter(house__building__community=request.user.community)
        houses = House.objects.filter(building__community=request.user.community)
    else:
        payments = PaymentRecord.objects.all()
        houses = House.objects.all()

    # 新增缴费记录（物业/超级管理员）
    if request.method == 'POST' and request.user.role in ['property_admin', 'super_admin']:
        house_id = request.POST.get('house')
        payment_type = request.POST.get('payment_type')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')

        house = get_object_or_404(House, id=house_id)
        PaymentRecord.objects.create(
            house=house,
            payment_type=payment_type,
            amount=amount,
            payer=house.owner if house.owner else request.user,
            payment_method=payment_method
        )
        messages.success(request, '缴费记录添加成功')
        return redirect('payments-list')

    context = {'payments': payments}
    if request.user.role in ['property_admin', 'super_admin']:
        context['houses'] = houses
        context['payment_types'] = PaymentRecord.PAYMENT_TYPE

    return render(request, 'property/payment_list.html', context)




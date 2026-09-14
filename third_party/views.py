from django.shortcuts import render
from django.http import JsonResponse
from .base import mock_payment_api, mock_access_api

# 支付接口页面
def payment_page(request):
    if request.method == 'POST':
        # 获取表单参数
        house_id = request.POST.get('house_id')
        amount = float(request.POST.get('amount', 0))
        payment_type = request.POST.get('payment_type')
        # 调用模拟支付接口
        result = mock_payment_api(house_id, amount, payment_type)
        return JsonResponse(result)
    # GET请求返回页面
    return render(request, 'third_party/payment.html')

# 门禁接口页面
def access_page(request):
    if request.method == 'POST':
        # 获取表单参数
        house_id = request.POST.get('house_id')
        user_id = request.POST.get('user_id')
        # 调用模拟门禁接口
        result = mock_access_api(house_id, user_id)
        return JsonResponse(result)
    # GET请求返回页面
    return render(request, 'third_party/access.html')
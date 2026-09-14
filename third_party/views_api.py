from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .base import mock_payment_api, mock_access_api

# 第三方支付API ViewSet
class PaymentApiViewSet(viewsets.ViewSet):
    # 模拟支付接口（POST请求）
    @action(detail=False, methods=['post'])
    def pay(self, request):
        house_id = request.data.get('house_id')
        amount = float(request.data.get('amount', 0))
        payment_type = request.data.get('payment_type')
        result = mock_payment_api(house_id, amount, payment_type)
        return Response(result)

# 第三方门禁API ViewSet
class AccessApiViewSet(viewsets.ViewSet):
    # 模拟门禁授权接口（POST请求）
    @action(detail=False, methods=['post'])
    def authorize(self, request):
        house_id = request.data.get('house_id')
        user_id = request.data.get('user_id')
        result = mock_access_api(house_id, user_id)
        return Response(result)
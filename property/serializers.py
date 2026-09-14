from rest_framework import serializers
from .models import RepairOrder, Notice, PaymentRecord

class RepairOrderSerializer(serializers.ModelSerializer):
    reporter_name = serializers.CharField(source='reporter.username', read_only=True)
    handler_name = serializers.CharField(source='handler.username', read_only=True)
    house_info = serializers.CharField(source='house.__str__', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = RepairOrder
        fields = '__all__'

class NoticeSerializer(serializers.ModelSerializer):
    publisher_name = serializers.CharField(source='publisher.username', read_only=True)
    community_name = serializers.CharField(source='community.name', read_only=True)

    class Meta:
        model = Notice
        fields = '__all__'

class PaymentRecordSerializer(serializers.ModelSerializer):
    payer_name = serializers.CharField(source='payer.username', read_only=True)
    house_info = serializers.CharField(source='house.__str__', read_only=True)
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)

    class Meta:
        model = PaymentRecord
        fields = '__all__'
from rest_framework import serializers
from .models import Community, Building, House

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class BuildingSerializer(serializers.ModelSerializer):
    community_name = serializers.CharField(source='community.name', read_only=True)

    class Meta:
        model = Building
        fields = '__all__'

class HouseSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source='building.name', read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = House
        fields = '__all__'
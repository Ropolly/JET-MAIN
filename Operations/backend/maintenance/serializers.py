from rest_framework import serializers
from .models import Aircraft, MaintenanceLog


class MaintenanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceLog
        fields = '__all__'


class AircraftSerializer(serializers.ModelSerializer):
    maintenance_logs = MaintenanceLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = Aircraft
        fields = '__all__'


class AircraftStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['status', 'notes']

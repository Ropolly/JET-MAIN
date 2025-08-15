from rest_framework import serializers
from .models import IndexPage


class IndexPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexPage
        fields = '__all__'

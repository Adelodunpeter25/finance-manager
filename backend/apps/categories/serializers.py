from rest_framework import serializers
from tracker.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'created_at']
        read_only_fields = ['id', 'created_at']

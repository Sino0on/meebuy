from rest_framework import serializers
from apps.provider.models import Category


class CategoryListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField(method_name='children_func')
    name = serializers.CharField(source='title')

    def children_func(self, obj):
        if obj.categor.all().exists():
            print(CategoryListSerializer(obj.categor.all(), many=True).data)
            return CategoryListSerializer(obj.categor.all(), many=True).data

    class Meta:
        model = Category
        fields = ['id', 'icon', 'name', 'category', 'children']

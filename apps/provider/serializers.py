from rest_framework import serializers
from apps.provider.models import Category


class CategoryListSerializer(serializers.ModelSerializer):
    is_selected = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    def get_is_selected(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj in request.user.categories.all()
        return False

    def get_children(self, obj):
        if obj.children.all().exists():
            return CategoryListSerializer(obj.children.all(), many=True, context=self.context).data
        return []

    class Meta:
        model = Category
        fields = ['id', 'icon', 'name', 'children', 'is_selected']

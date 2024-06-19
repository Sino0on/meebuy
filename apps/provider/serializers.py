from rest_framework import serializers

from apps.provider.models import Category


class CategoryListSerializer(serializers.ModelSerializer):
    is_selected = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    def get_is_selected(self, obj):
        user_categories = self.context.get('categories', [])
        return obj in user_categories

    def get_children(self, obj):
        children = obj.categor.all()
        if children.exists():
            serializer = CategoryListSerializer(children, many=True, context=self.context)
            return serializer.data
        return []

    class Meta:
        model = Category
        fields = ['id', 'title', 'icon', 'children', 'is_selected']

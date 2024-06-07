from rest_framework import serializers
from apps.provider.models import Category

class CategoryListSerializer(serializers.ModelSerializer):
    is_selected = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    def get_is_selected(self, obj):
        # Из контекста получаем категории, выбранные пользователем
        user_categories = self.context.get('categories', [])
        # Проверяем, содержится ли текущий объект категории в списке выбранных категорий
        return obj in user_categories

    def get_children(self, obj):
        # Получаем дочерние категории используя related_name 'categor'
        if obj.categor.all().exists():
            # Рекурсивно сериализуем дочерние категории, если они существуют
            return CategoryListSerializer(obj.categor.all(), many=True, context=self.context).data
        return []

    class Meta:
        model = Category
        # Используем 'title' вместо 'name', если в модели это поле называется 'title'
        fields = ['id', 'title', 'icon', 'children', 'is_selected']

from rest_framework import serializers

from apps.user_cabinet.models import Status, PackageStatus


class PackageStatusSerializer(serializers.ModelSerializer):
    per_month = serializers.SerializerMethodField(method_name='per_month_func')

    def per_month_func(self, obj):
        return obj.get_month_price()

    class Meta:
        model = PackageStatus
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    statuses = PackageStatusSerializer(many=True, source='packagestatuses')

    class Meta:
        model = Status
        fields = '__all__'
        include = ('statuses',)

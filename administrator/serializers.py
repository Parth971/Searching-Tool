from datetime import datetime

from django.conf import settings
from rest_framework import serializers

from administrator.constants import MONTHLY, YEARLY
from search.constants import DEFAULT_IMAGE_PATH
from search.models import Framework, Cpv, Document, LOT, Supplier


class DurationSerializer(serializers.Serializer):
    date_formats = [MONTHLY, YEARLY]
    duration = serializers.ChoiceField(choices=date_formats)

    def validate_duration(self, value):
        if value not in self.date_formats:
            raise serializers.ValidationError("Invalid duration. Must be 'monthly' or 'yearly'.")
        return value


class CpvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cpv
        fields = ('code',)


class CpvListSerializer(serializers.ListSerializer):
    child = CpvSerializer()

    def to_representation(self, data):
        return data.values_list('code', flat=True)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('name', 'link')


class LOTSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOT
        fields = ('name', 'description')


class FrameworkDetailSerializer(serializers.ModelSerializer):
    cpvs = CpvListSerializer(child=CpvSerializer())
    documents = DocumentSerializer(many=True)
    lots = LOTSerializer(many=True)

    class Meta:
        model = Framework
        fields = [
            'id', 'name', 'number', 'value', 'start_date',
            'end_date', 'service_type', 'description', 'logo',
            'industry_or_category', 'sub_category', 'cpvs',
            'documents', 'lots'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['logo'] is None:
            representation['logo'] = DEFAULT_IMAGE_PATH % settings.BACK_END_DOMAIN
        else:
            representation['logo'] = settings.BACK_END_DOMAIN + settings.MEDIA_URL + representation['logo']

        return representation

from rest_framework import serializers
from .models import Tag, Feature, Banner


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    tag_ids = TagSerializer(many=True, read_only=True)
    feature_id = FeatureSerializer(read_only=True)

    class Meta:
        model = Banner
        fields = ['tag_ids', 'feature_id', 'content', 'created_at', 'updated_at']


class BannerDetailSerializer(serializers.ModelSerializer):
    feature_id = FeatureSerializer()

    class Meta:
        model = Banner
        fields = ['tag_ids', 'feature_id', 'content', 'is_active', 'created_at', 'updated_at']

from rest_framework import serializers
from .models import Tag, Feature, Banner, VoidModel


class VoidSer(serializers.ModelSerializer):
    class Meta:
        model = VoidModel
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class BannerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ['content']  # убрать ид
        extra_kwargs = {
            'is_active': {'write_only': True},
        }


class BannerSerializer(serializers.ModelSerializer):
    tag_ids = TagSerializer(many=True, read_only=True)
    feature_id = FeatureSerializer(read_only=True)

    class Meta:
        model = Banner
        fields = ['tag_ids', 'feature_id', 'content', 'created_at', 'updated_at']
        extra_kwargs = {
            'tag_ids': {'write_only': True},
            'feature_id': {'write_only': True},
            'content': {'write_only': True},
            'is_active': {'write_only': True},
        }


class BannerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['tag_ids', 'feature_id', 'content', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')
        """extra_kwargs = {
            'tag_ids': {'write_only': True},
            'feature_id': {'write_only': True},
            'content': {'write_only': True},
            'is_active': {'write_only': True},
        }"""

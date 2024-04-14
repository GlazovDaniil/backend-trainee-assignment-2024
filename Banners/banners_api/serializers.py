from rest_framework import serializers
from .models import Tag, Feature, Banner


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели тега
    """
    class Meta:
        model = Tag
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели фичи
    """
    class Meta:
        model = Feature
        fields = '__all__'


class BannerUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели баннера для пользователя
    """
    class Meta:
        model = Banner
        fields = ['content']  # убрать ид
        extra_kwargs = {
            'is_active': {'write_only': True},
        }


class BannerSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели баннера
    """
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
    """
    Сериализатор модели баннера для представлений администратора
    """
    class Meta:
        model = Banner
        fields = ['tag_ids', 'feature_id', 'content', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')

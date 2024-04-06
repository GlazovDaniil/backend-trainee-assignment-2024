from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .models import Banner, Tag, VoidModel, Feature
from .serializers import (BannerSerializer, BannerDetailSerializer, VoidSer, TagSerializer, FeatureSerializer,
                          BannerUserSerializer)
from .permissions import IsAdmin
from django.core.cache import cache
from .castom_exeptions import MyCustomException
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser



class VoidAPI(generics.CreateAPIView):
    model = VoidModel
    serializer_class = VoidSer
    queryset = VoidModel.objects.all()


class TagCreateAPIView(generics.CreateAPIView):
    model = Tag
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAdmin,)

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, serializer.validated_data)
        serializer.save()


class FeatureCreateAPIView(generics.CreateAPIView):
    model = Feature
    serializer_class = FeatureSerializer
    queryset = Feature.objects.all()
    permission_classes = (IsAdmin,)

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, serializer.validated_data)
        serializer.save()


class UserBannerAPIView(generics.ListAPIView):
    model = Banner
    serializer_class = BannerUserSerializer

    def get_queryset(self):
        # Фильтруем выдачу во входным данным
        tag_id = self.request.query_params.get("tag_id")
        feature_id = self.request.query_params.get("feature_id")
        use_last_revision = self.request.query_params.get("use_last_revision", False)

        if use_last_revision:
            # Получить самую актуальную информацию
            return Banner.objects.filter(is_active=True, tag_ids=tag_id, feature_id=feature_id)
        else:
            # Получить закешированную информацию, которая была актуальна 5 минут назад
            banner = cache.get('banner')
            if banner is None:
                banner = Banner.objects.filter(is_active=True, tag_ids=tag_id, feature_id=feature_id)
                cache.set('banner', banner, 60 * 5)
            return banner


class BannerAPIView(generics.CreateAPIView, generics.ListAPIView):
    model = Banner
    serializer_class = BannerDetailSerializer
    permission_classes = (IsAdminUser,)
    ordering = ['-updated_at']

    def get(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return self.list(request, *args, **kwargs)
        else:
            raise MyCustomException(detail={"description": "Пользователь не имеет доступа"},
                                    status_code=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        queryset = Banner.objects.all()

        feature_id = self.request.query_params.get('feature_id')
        tag_id = self.request.query_params.get('tag_id')

        if feature_id:
            queryset = queryset.filter(feature_id=feature_id)
        if tag_id:
            queryset = queryset.filter(tag_ids=tag_id)

        limit = self.request.query_params.get('limit')
        offset = self.request.query_params.get('offset')

        if limit:
            queryset = queryset[:int(limit)]
        if offset:
            queryset = queryset[int(offset):]

        return queryset

    def post(self, request, *args, **kwargs):
        tag_id = request.data['tag_ids']
        feature_id = request.data['feature_id']
        banner = Banner.objects.filter(is_active=True, tag_ids=tag_id, feature_id=feature_id)
        if banner:
            raise MyCustomException(detail={"description": "Некорректные данные"},
                                    status_code=status.HTTP_400_BAD_REQUEST)
        else:
            return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, serializer.validated_data)
        serializer.save()


class BannerDetailAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    model = Banner
    serializer_class = BannerDetailSerializer
    queryset = Banner.objects.all()
    permission_classes = (IsAdmin,)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')


def accounts_profile_redirect(request):
    return HttpResponseRedirect('/user_banner/')

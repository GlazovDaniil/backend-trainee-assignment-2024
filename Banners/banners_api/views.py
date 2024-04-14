from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .models import Banner, Tag, Feature
from .serializers import BannerDetailSerializer, TagSerializer, FeatureSerializer, BannerUserSerializer
from .permissions import IsAdmin
from django.core.cache import cache
from .castom_exeptions import MyCustomException
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TagCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания тегов

    Права доступа только для администраторов и суперпользователя
    """
    model = Tag
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAdmin,)

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, serializer.validated_data)
        serializer.save()


class FeatureCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания фич

    Права доступа только для администраторов и суперпользователя
    """
    model = Feature
    serializer_class = FeatureSerializer
    queryset = Feature.objects.all()
    permission_classes = (IsAdmin,)

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, serializer.validated_data)
        serializer.save()


class UserBannerAPIView(generics.ListAPIView):
    """
    Представление для просмотра пользователем баннеров

    С правами доступа для всех зарегистрированных пользователей
    """
    model = Banner
    serializer_class = BannerUserSerializer

    """@swagger_auto_schema(manual_parameters=[
        openapi.Parameter('tag_id', openapi.IN_QUERY, description='feature_id', type=openapi.TYPE_INTEGER),
        openapi.Parameter('feature_id', openapi.IN_QUERY, description='feature_id', type=openapi.TYPE_INTEGER),
        openapi.Parameter('use_last_revision', openapi.IN_QUERY, description='use_last_revision',
                          type=openapi.TYPE_BOOLEAN),
    ])"""
    def get(self, request, *args, **kwargs):
        """
        Позволяет вывести в swagger ожидаемые параметры query
        """
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Метод кеширования и вывода часто используемых баннеров
        с учетом флага use_last_revision,
        при значении True которого используется актуальная информация из БД
        """
        tag_id = self.request.query_params.get("tag_id")
        feature_id = self.request.query_params.get("feature_id")
        use_last_revision = self.request.query_params.get("use_last_revision", False)

        if use_last_revision:
            banner = Banner.objects.filter(is_active=True, tag_ids=tag_id, feature_id=feature_id)
        else:
            banner = cache.get(f'{feature_id}-{feature_id}')
            if banner is None:
                banner = Banner.objects.filter(is_active=True, tag_ids=tag_id, feature_id=feature_id)
                cache.set(f'{feature_id}-{feature_id}', banner, 60 * 5)

        if banner:
            return banner
        else:
            raise MyCustomException(detail={"description": "Баннер для не найден"},
                                    status_code=status.HTTP_404_NOT_FOUND)


class BannerAPIView(generics.ListCreateAPIView):
    """
    Представление создания баннера и просмотра списка всех баннеров без учета флага is_active

    Права доступа только для администраторов и суперпользователя
    """
    model = Banner
    serializer_class = BannerDetailSerializer
    permission_classes = (IsAdminUser,)
    ordering = ['-updated_at']

    def get_queryset(self):
        """
        Определение набора выходных данных с учетом query параметров
        """
        queryset = Banner.objects.all()

        if feature_id := self.request.query_params.get('feature_id'):
            queryset = queryset.filter(feature_id=feature_id)
        if tag_id := self.request.query_params.get('tag_id'):
            queryset = queryset.filter(tag_ids=tag_id)

        if limit := self.request.query_params.get('limit'):
            queryset = queryset[:int(limit)]
        if offset := self.request.query_params.get('offset'):
            queryset = queryset[int(offset):]

        return queryset

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('tag_id', openapi.IN_QUERY, description='feature_id', type=openapi.TYPE_INTEGER),
        openapi.Parameter('feature_id', openapi.IN_QUERY, description='feature_id', type=openapi.TYPE_INTEGER),
        ])
    def get(self, request, *args, **kwargs):
        """
        Позволяет вывести в swagger ожидаемые параметры query;

        Проверяет права доступа для GET запроса
        (является ли администратором или суперпользователем)
        """
        if request.user.is_staff or request.user.is_superuser:
            return self.list(request, *args, **kwargs)
        else:
            raise MyCustomException(detail={"description": "Пользователь не имеет доступа"},
                                    status_code=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        """
        Проверка создаваемого баннера на конфликт тегов и фич,
        так как баннер должен однозначно определяться парой тег, фича.
        """
        tag_id = list(request.data['tag_ids'])
        feature_id = request.data['feature_id']
        banner = Banner.objects.filter(is_active=True, tag_ids__in=tag_id, feature_id=feature_id)
        if banner:
            raise MyCustomException(detail={"description": "Некорректные данные. "
                                                           "Нарушается правило однозначности баннеров."},
                                    status_code=status.HTTP_400_BAD_REQUEST)
        else:
            return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Служит для проверки доступа пользователя к POST запросу
        (является ли администратором или суперпользователем)
        """
        self.check_object_permissions(self.request, serializer.validated_data)
        serializer.save()


class BannerDetailAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    Представление для изменения и удаления баннеров по pk
    """
    model = Banner
    serializer_class = BannerDetailSerializer
    queryset = Banner.objects.all()
    permission_classes = (IsAdmin,)


def logout_view(request):
    """
    Представление для выхода аккаунта API
    """
    logout(request)
    return HttpResponseRedirect('/auth/login/')


def accounts_profile_redirect(request):
    """
    Перенаправляет на странице пользовательского банера
    """
    return HttpResponseRedirect('/user_banner/')

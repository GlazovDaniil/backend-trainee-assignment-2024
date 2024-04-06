from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (logout_view, accounts_profile_redirect, UserBannerAPIView, BannerAPIView, BannerDetailAPIView,
                    TagCreateAPIView, FeatureCreateAPIView, VoidAPI)


urlpatterns = [
    path('void_create/', VoidAPI.as_view()),
    path('tag/create/', TagCreateAPIView.as_view()),
    path('feature/create/', FeatureCreateAPIView.as_view()),

    path('api-authlogout/', logout_view),  # затычка
    path('accounts/profile/', accounts_profile_redirect),  # затычка

    path('user_banner/', UserBannerAPIView.as_view()),  # get
    path('banner/<int:pk>/', BannerDetailAPIView.as_view()),  # patch, delete
    path('banner/', BannerAPIView.as_view()),  # get, post
]
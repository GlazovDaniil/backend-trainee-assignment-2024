from django.urls import path
from .views import logout_view, accounts_profile_redirect, UserBannerAPIView, BannerAPIView, BannerDetailAPIView


urlpatterns = [
    path('api-authlogout/', logout_view),  # затычка
    path('accounts/profile/', accounts_profile_redirect),  # затычка
    path('user_banner/', UserBannerAPIView.as_view()),  # get
    path('banner/<int:pk>/', BannerDetailAPIView.as_view()),  # patch, delete
    path('banner/', BannerAPIView.as_view()),  # get, post
]
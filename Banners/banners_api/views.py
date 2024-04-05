from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from rest_framework import generics
from .models import Banner
from .serializers import BannerSerializer, BannerDetailSerializer
from .permissions import IsAdminOrReadonly


class UserBannerAPIView(generics.ListAPIView):
    model = Banner
    serializer_class = BannerSerializer
    queryset = Banner.objects.filter(is_active=True)


class BannerAPIView(generics.ListAPIView, generics.ListCreateAPIView):
    model = Banner
    serializer_class = BannerSerializer
    queryset = Banner.objects.filter(is_active=True)
    permission_classes = IsAdminOrReadonly,


class BannerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    model = Banner
    serializer_class = BannerDetailSerializer
    queryset = Banner.objects.all()
    permission_classes = IsAdminOrReadonly,


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/api-authlogin/')


def accounts_profile_redirect(request):
    return HttpResponseRedirect('/user_banner/')

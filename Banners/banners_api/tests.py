from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from .models import Tag, Feature, Banner
import json

class BannerIntegrationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание пользователей (админ и простой пользователь)
        test_admin = User.objects.create_user(
            username='test_admin',
            password='abc123',
            is_staff=True,
        )
        test_admin.save()
        test_user = User.objects.create_user(
            username='test_user',
            password='abc123',
        )
        test_user.save()

        # Создание тегов
        test_tag1 = Tag.objects.create(name=f'test_tag1')
        test_tag2 = Tag.objects.create(name=f'test_tag2')
        test_tag3 = Tag.objects.create(name=f'test_tag3')
        test_tag4 = Tag.objects.create(name=f'test_tag4')

        test_feature1 = Feature.objects.create(name=f'test_feature1')
        test_feature2 = Feature.objects.create(name=f'test_feature2')
        test_feature3 = Feature.objects.create(name=f'test_feature3')

        test_feature3.save()

        test_banner1 = Banner.objects.create(
            feature_id=test_feature1,
            content={'text': 'Banner 1'},
            is_active=True,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        test_banner1.tag_ids.add(test_tag1)
        test_banner1.tag_ids.add(test_tag2)
        test_banner1.save()

        test_banner2 = Banner.objects.create(
            feature_id=test_feature1,
            content={'text': 'Banner 2'},
            is_active=True,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        test_banner1.tag_ids.add(test_tag4)
        test_banner2.save()

        test_banner3 = Banner.objects.create(
            feature_id=test_feature2,
            content={'text': 'Banner 3'},
            is_active=False,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        test_banner1.tag_ids.add(test_tag1)
        test_banner1.tag_ids.add(test_tag2)
        test_banner1.tag_ids.add(test_tag3)
        test_banner1.tag_ids.add(test_tag4)
        test_banner3.save()

    def test_get_banner_user(self, token: str, parameters: dict):
        print('- Получение токена')
        response = self.client.post("/auth/login/", {"username": "test_user", "password": "abc123"})
        self.assertEqual(response.status_code, 200, "Токен должен быть успешно возвращен.")
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content["auth_token"]
        print('- Токен получен')
        response = self.client.get("/user_banner/", parameters,
                                   HTTP_AUTHORIZATION='Token {0}'.format(token))
        self.assertEquals(response.status_code, 200)

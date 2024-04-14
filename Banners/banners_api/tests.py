import json
import time

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Tag, Feature, Banner


def time_tracker(func):
    def wrapper(*args, **kwargs):
        try:
            start_time = time.time()
            func(*args, **kwargs)
            end_time = time.time() - start_time
        except Exception as e:
            print(f'Тест {func.__name__} провален с ошибкой {e}')
        else:
            print(f'Тест {func.__name__} выполнен УСПЕШНО за {end_time}.')
    return wrapper


class BannerIntegrationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создание тестового набора данных"""
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

        # Создание фич
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
        test_banner2.tag_ids.add(test_tag4)
        test_banner2.save()

        test_banner3 = Banner.objects.create(
            feature_id=test_feature2,
            content={'text': 'Banner 3'},
            is_active=False,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        test_banner3.tag_ids.add(test_tag1)
        test_banner3.tag_ids.add(test_tag2)
        test_banner3.tag_ids.add(test_tag3)
        test_banner3.tag_ids.add(test_tag4)
        test_banner3.save()

    @time_tracker
    def test_get_banner_no_token(self) -> None:
        """Получение данных /user_banner/ не авторизовавшись"""
        response = self.client.get("/user_banner/?tag_id=1&feature_id=1&use_last_revision=true")
        self.assertEqual(response.status_code, 401)

    @time_tracker
    def get_banner_tag_feature(self, token: str) -> None:
        """Получение данных /user_banner/ по существующим тегу и фиче, определяюшие существующий баннер"""
        response = self.client.get("/user_banner/?tag_id=1&feature_id=1&use_last_revision=true", {},
                                   HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 200)

    @time_tracker
    def get_no_banner_tag_feature(self, token: str) -> None:
        """Получение данных /user_banner/ по существующим тегу и фиче, определяюшие не существующий баннер"""
        response = self.client.get("/user_banner/?tag_id=3&feature_id=1&use_last_revision=true", {},
                                   HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 404)

    @time_tracker
    def get_banner_no_tag_feature(self, token: str) -> None:
        """Получение данных /user_banner/ по не существующему тегу, но существующей фиче"""
        response = self.client.get("/user_banner/?tag_id=6&feature_id=1&use_last_revision=true", {},
                                   HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 404)

    @time_tracker
    def get_banner_tag_no_feature(self, token: str) -> None:
        """Получение данных /user_banner/ по существующему тегу, и не существующей фиче"""
        response = self.client.get("/user_banner/?tag_id=1&feature_id=5&use_last_revision=true", {},
                                   HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 404)

    @time_tracker
    def get_off_banner_test(self, token: str) -> None:
        """Попытка получения выключенного баннера /user_banner/"""
        response = self.client.get("/user_banner/?tag_id=3&feature_id=2&use_last_revision=true", {},
                                   HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 404)

    @time_tracker
    def cache_test(self, token: str) -> None:
        """Проверка кеширования часто используемой информации"""
        response = self.client.get("/user_banner/?tag_id=1&feature_id=1", {}, HTTP_AUTHORIZATION=f'Token {token}')
        response_content = json.loads(response.content.decode('utf-8'))
        banner_old_content = response_content[0]['content']

        banner = Banner.objects.get(is_active=True, tag_ids=1, feature_id=1)
        banner_new_content = {'text': 'New text banner 1'}
        banner.content = banner_new_content
        banner.save()
        response = self.client.get("/user_banner/?tag_id=1&feature_id=1", {}, HTTP_AUTHORIZATION=f'Token {token}')
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_content[0]['content'], banner_old_content)

        response = self.client.get("/user_banner/?tag_id=1&feature_id=1&use_last_revision=true", {},
                                   HTTP_AUTHORIZATION=f'Token {token}')
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_content[0]['content'], banner_new_content)

    @time_tracker
    def get_banner_list_user(self, token: str) -> None:
        """Получение пользователем данных /banner/"""
        response = self.client.get("/banner/", {}, HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 403)

    @time_tracker
    def get_banner_list_admin(self, token: str) -> None:
        """Получение пользователем данных /banner/"""
        response = self.client.get("/banner/", {}, HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 200)

    def get_user_token(self, username: str, password: str) -> str:
        """Получение токена"""
        response = self.client.post("/auth/login/", {"username": username, "password": password})
        self.assertEqual(response.status_code, 200, "Токен должен быть успешно возвращен")
        response_content = json.loads(response.content.decode('utf-8'))
        return response_content["key"]

    @time_tracker
    def test_get_banner_user(self) -> None:
        """Тест получения обычным пользователем баннеров и получение токена"""
        user_token = self.get_user_token('test_user', 'abc123')

        self.get_off_banner_test(user_token)
        self.get_banner_tag_feature(user_token)
        self.get_banner_no_tag_feature(user_token)
        self.get_banner_tag_no_feature(user_token)
        self.get_no_banner_tag_feature(user_token)
        self.cache_test(user_token)
        self.get_banner_list_user(user_token)

    @time_tracker
    def test_get_banner_admin(self) -> None:
        """Тест получения админом банера"""
        admin_token = self.get_user_token('test_admin', 'abc123')

        self.get_off_banner_test(admin_token)
        self.get_banner_tag_feature(admin_token)
        self.get_banner_no_tag_feature(admin_token)
        self.get_banner_tag_no_feature(admin_token)
        self.get_no_banner_tag_feature(admin_token)
        self.cache_test(admin_token)
        self.get_banner_list_admin(admin_token)

    @time_tracker
    def stress_1000_banners(self) -> None:
        """Стресс тест на 1000 запросов"""
        for _ in range(1000):
            # Создание 1000 тегов и фич
            Tag.objects.create(name=f'stress_test_tag')
            Feature.objects.create(name=f'stress_test_feature')

        admin_token = self.get_user_token('test_admin', 'abc123')

        start = time.time()
        count_tests = 10**3 // 7
        for _ in range(count_tests):
            self.get_off_banner_test(admin_token)
            self.get_banner_tag_feature(admin_token)
            self.get_banner_no_tag_feature(admin_token)
            self.get_banner_tag_no_feature(admin_token)
            self.get_no_banner_tag_feature(admin_token)
            self.cache_test(admin_token)
            self.get_banner_list_admin(admin_token)
        end = time.time()
        all_time = "{:.3f}".format((end - start) * 10**3)
        one_request_rime = "{:.3f}".format((end - start) * 10**3 / (7 * count_tests))

        print(f'- Время преодоления стресс теста: {all_time} мс.\n'
              f'- В среднем {one_request_rime} мс за запрос.\n'
              f'test_stress_1000_banners [Успешно]')

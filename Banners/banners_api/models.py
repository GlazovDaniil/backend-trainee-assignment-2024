from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=25, help_text='Введите название тега', verbose_name='Название тега')

    def __str__(self):
        return str(self.name)


class Feature(models.Model):
    name = models.CharField(max_length=25, help_text='Введите название фичи', verbose_name='Название фичи')

    def __str__(self):
        return str(self.name)


class Banner(models.Model):
    feature_id = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='feature',
                                   help_text='Введите название бане',
                                   verbose_name='Название')
    tag_ids = models.ManyToManyField(Tag, related_name='tags',
                                     help_text='Выберите теги пользователя',
                                     verbose_name='Тэг пользователя')
    content = models.JSONField(verbose_name="Содержимое баннера")
    is_active = models.BooleanField(default=True, help_text='Выберите флаг активности баннера',
                                    verbose_name='Флаг активности баннера')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания баннера')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления баннера')

    def __str__(self):
        return str(self.content)

    def get_is_active(self):
        return self.is_active

# Generated by Django 4.2.11 on 2024-04-08 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banners_api', '0002_voidmodel_alter_banner_is_active'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VoidModel',
        ),
        migrations.AlterField(
            model_name='banner',
            name='feature_id',
            field=models.ForeignKey(help_text='Выберите фичу', on_delete=django.db.models.deletion.CASCADE, related_name='feature', to='banners_api.feature', verbose_name='Фича'),
        ),
    ]
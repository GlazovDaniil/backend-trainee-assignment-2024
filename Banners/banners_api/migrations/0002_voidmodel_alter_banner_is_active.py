# Generated by Django 4.2.11 on 2024-04-05 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoidModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='banner',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Выберите флаг активности баннера', verbose_name='Флаг активности баннера'),
        ),
    ]
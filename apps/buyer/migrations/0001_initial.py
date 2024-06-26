# Generated by Django 4.2.11 on 2024-06-13 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=123, null=True, verbose_name='Телефон')),
                ('image_desktop', models.ImageField(upload_to='images/banners/desktop/%Y/%m/', verbose_name='Картинка круп')),
                ('image_mobile', models.ImageField(upload_to='images/banners/mobile/%Y/%m/', verbose_name='Картинка моб')),
                ('page_for', models.CharField(choices=[('provider', 'Поставщики'), ('tender', 'Закупки'), ('buyer', 'Покупатели')], default='provider', max_length=200, verbose_name='Страница')),
                ('link', models.URLField(blank=True, null=True, verbose_name='ссылка')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
                'ordering': ['is_active', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BannerSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=3, verbose_name='Очередность')),
            ],
            options={
                'verbose_name': 'Очередность',
            },
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=123, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('mini_desc', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/avatars/buyer/')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=123, null=True)),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BuyerImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/buyer/%Y/%m/')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='buyer.buyer')),
            ],
            options={
                'verbose_name': 'Изображение Продавца',
                'verbose_name_plural': 'Изображения Продавца',
            },
        ),
        migrations.CreateModel(
            name='BuyerFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/providers/%Y/%m/')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='buyer.buyer')),
            ],
            options={
                'verbose_name': 'Файл Продавца',
                'verbose_name_plural': 'Файлы Продавца',
            },
        ),
    ]

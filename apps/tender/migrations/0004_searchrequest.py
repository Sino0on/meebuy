# Generated by Django 4.2.11 on 2024-06-17 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tender', '0003_country_code_alter_tender_category_alter_tender_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now=True)),
                ('name', models.TextField(blank=True, null=True, verbose_name='Запрос')),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='search_requests', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
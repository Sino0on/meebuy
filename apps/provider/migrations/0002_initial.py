# Generated by Django 4.2.11 on 2024-06-13 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tender', '0001_initial'),
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tender.city'),
        ),
        migrations.AddField(
            model_name='provider',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='provider.tag', verbose_name='Тип'),
        ),
        migrations.AddField(
            model_name='provider',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='provideimg',
            name='providers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='provider.provider'),
        ),
        migrations.AddField(
            model_name='providefiles',
            name='providers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='provider.provider'),
        ),
        migrations.AddField(
            model_name='pricefiles',
            name='providers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files_price', to='provider.provider'),
        ),
        migrations.AddField(
            model_name='category',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categor', to='provider.category', verbose_name='Родительская категория'),
        ),
    ]

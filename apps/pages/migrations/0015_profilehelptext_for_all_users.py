# Generated by Django 4.2.11 on 2024-10-10 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_profilehelptext_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilehelptext',
            name='for_all_users',
            field=models.BooleanField(default=False, verbose_name='Для всех пользователей'),
        ),
    ]

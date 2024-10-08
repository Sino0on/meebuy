# Generated by Django 4.2.11 on 2024-10-03 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_telegrambottoken_support_telegram_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterColumn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='FooterLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('link', models.URLField(verbose_name='Ссылка')),
                ('order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]

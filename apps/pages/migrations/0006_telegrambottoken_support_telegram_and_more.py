# Generated by Django 4.2.11 on 2024-09-19 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_telegrambottoken_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegrambottoken',
            name='support_telegram',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Telegram поддержки'),
        ),
        migrations.AddField(
            model_name='telegrambottoken',
            name='support_whatsapp',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='WhatsApp поддержки'),
        ),
    ]

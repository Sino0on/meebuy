# Generated by Django 4.2.11 on 2024-06-19 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_cabinet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packagestatus',
            name='dayly_message',
        ),
        migrations.RemoveField(
            model_name='packagestatus',
            name='image',
        ),
        migrations.RemoveField(
            model_name='packagestatus',
            name='is_advertise',
        ),
        migrations.RemoveField(
            model_name='packagestatus',
            name='is_contact_prov',
        ),
        migrations.RemoveField(
            model_name='packagestatus',
            name='is_email',
        ),
        migrations.RemoveField(
            model_name='packagestatus',
            name='is_publish_phone',
        ),
        migrations.RemoveField(
            model_name='packagestatus',
            name='quantity_products',
        ),
        migrations.RemoveField(
            model_name='packagestatus',
            name='quantity_tenders',
        ),
        migrations.AddField(
            model_name='activeuserstatus',
            name='start_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата начала'),
        ),
        migrations.AddField(
            model_name='status',
            name='dayly_message',
            field=models.PositiveIntegerField(blank=True, default=30, verbose_name='Исходящих сообщений в день'),
        ),
        migrations.AddField(
            model_name='status',
            name='image',
            field=models.FileField(blank=True, default='1', upload_to='images/packages/', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='status',
            name='is_advertise',
            field=models.BooleanField(blank=True, default=False, verbose_name='Просмотр сайта без рекламы'),
        ),
        migrations.AddField(
            model_name='status',
            name='is_contact_prov',
            field=models.BooleanField(blank=True, default=False, verbose_name='Просмотр контактов поставщиков'),
        ),
        migrations.AddField(
            model_name='status',
            name='is_email',
            field=models.BooleanField(blank=True, default=False, verbose_name='Показ Вашего E-mail и ссылки на ваш сайт / соцсети'),
        ),
        migrations.AddField(
            model_name='status',
            name='is_publish_phone',
            field=models.BooleanField(blank=True, default=False, verbose_name='Показ Вашего телефона незарегистрированным посетителям'),
        ),
        migrations.AddField(
            model_name='status',
            name='quantity_products',
            field=models.PositiveIntegerField(default=2, verbose_name='Количество объявлений'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status',
            name='quantity_tenders',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество закупок'),
            preserve_default=False,
        ),
    ]

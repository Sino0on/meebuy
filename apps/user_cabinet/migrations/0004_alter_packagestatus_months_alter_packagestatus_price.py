# Generated by Django 4.2.11 on 2024-06-21 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_cabinet', '0003_alter_status_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagestatus',
            name='months',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество месяцев'),
        ),
        migrations.AlterField(
            model_name='packagestatus',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=100, null=True, verbose_name='Цена'),
        ),
    ]

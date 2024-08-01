# Generated by Django 4.2.11 on 2024-08-01 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_product_large_wholesale_product_medium_wholesale_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='large_wholesale_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Цена за большую партию'),
        ),
        migrations.AddField(
            model_name='product',
            name='medium_wholesale_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Цена за среднюю партию'),
        ),
        migrations.AddField(
            model_name='product',
            name='small_wholesale_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Цена за малую партию'),
        ),
    ]

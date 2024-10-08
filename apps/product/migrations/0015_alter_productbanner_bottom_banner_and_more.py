# Generated by Django 4.2.11 on 2024-09-20 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_productcategory_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbanner',
            name='bottom_banner',
            field=models.FileField(blank=True, upload_to='images/banners/', verbose_name='Нижний баннер'),
        ),
        migrations.AlterField(
            model_name='productbanner',
            name='left_banner',
            field=models.FileField(blank=True, upload_to='images/banners/', verbose_name='Левый баннер'),
        ),
        migrations.AlterField(
            model_name='productbanner',
            name='right_banner',
            field=models.FileField(blank=True, upload_to='images/banners/', verbose_name='Правый баннер'),
        ),
        migrations.AlterField(
            model_name='productbanner',
            name='wide_banner',
            field=models.FileField(blank=True, upload_to='images/banners/', verbose_name='Широкий баннер'),
        ),
    ]

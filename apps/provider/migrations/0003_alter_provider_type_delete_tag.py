# Generated by Django 4.2.11 on 2024-06-13 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='type',
            field=models.CharField(blank=True, choices=[(1, 'Оптовая продажа товаров (вы поставщик)'), (2, 'Производство товаров (вы производитель)'), (3, 'Оказание услуг логистики / поиска товаров / таможенного оформления')], max_length=255, null=True, verbose_name='Тип'),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]

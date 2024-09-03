# Generated by Django 4.2.11 on 2024-09-02 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_cabinet', '0004_alter_packagestatus_months_alter_packagestatus_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='quantity_opening',
            field=models.PositiveIntegerField(default=10, verbose_name='Количество открытий'),
            preserve_default=False,
        ),
    ]

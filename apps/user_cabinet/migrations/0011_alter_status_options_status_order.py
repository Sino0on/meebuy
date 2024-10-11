# Generated by Django 4.2.11 on 2024-10-09 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_cabinet', '0010_rename_quantity_opening_tenders_cabinet_opened_tender_contacts'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['order'], 'verbose_name': 'Статус', 'verbose_name_plural': 'Статусы'},
        ),
        migrations.AddField(
            model_name='status',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
    ]

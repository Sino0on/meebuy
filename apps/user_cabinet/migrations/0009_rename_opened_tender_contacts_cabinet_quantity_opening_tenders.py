# Generated by Django 4.2.11 on 2024-09-09 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_cabinet', '0008_cabinet_base_tariff_connected_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cabinet',
            old_name='opened_tender_contacts',
            new_name='quantity_opening_tenders',
        ),
    ]

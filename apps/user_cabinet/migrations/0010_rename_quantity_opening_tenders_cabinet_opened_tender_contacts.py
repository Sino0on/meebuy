# Generated by Django 4.2.11 on 2024-09-09 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_cabinet', '0009_rename_opened_tender_contacts_cabinet_quantity_opening_tenders'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cabinet',
            old_name='quantity_opening_tenders',
            new_name='opened_tender_contacts',
        ),
    ]

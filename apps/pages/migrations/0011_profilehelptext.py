# Generated by Django 4.2.11 on 2024-10-10 05:49

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_telegrambottoken_recaptcha'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileHelpText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('text', ckeditor.fields.RichTextField(verbose_name='Текст')),
                ('button1_icon', models.FileField(upload_to='help_text/', verbose_name='Иконка 1')),
                ('button1_text', models.CharField(max_length=255, verbose_name='Кнопка 1')),
                ('button1_link', models.URLField(verbose_name='Ссылка 1')),
                ('button2_icon', models.FileField(upload_to='help_text/', verbose_name='Иконка 2')),
                ('button2', models.CharField(max_length=255, verbose_name='Кнопка 2')),
                ('button2_link', models.URLField(verbose_name='Ссылка 2')),
                ('order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]

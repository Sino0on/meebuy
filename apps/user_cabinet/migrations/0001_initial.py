# Generated by Django 4.2.11 on 2024-06-13 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
        ('tender', '0001_initial'),
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveUpping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ActiveUserStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateField(verbose_name='Дата окончание')),
                ('is_active', models.BooleanField(blank=True, default=False, verbose_name='Активный')),
            ],
            options={
                'verbose_name': 'Активный статус пользователя',
                'verbose_name_plural': 'Активные статусы пользователей',
            },
        ),
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.PositiveIntegerField(blank=True, default=0, verbose_name='Баланс')),
                ('favorite_products', models.ManyToManyField(blank=True, related_name='user_cabinet', to='product.product', verbose_name='Избранные продукты')),
                ('favorite_providers', models.ManyToManyField(blank=True, related_name='user_cabinet', to='provider.provider', verbose_name='Избранные оптовики')),
                ('favorite_tenders', models.ManyToManyField(blank=True, related_name='user_cabinet', to='tender.tender', verbose_name='Избранные закупки')),
                ('is_upping', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_cabinet.activeupping')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('user_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_statuses', to='user_cabinet.activeuserstatus', verbose_name='Статус пользователя')),
            ],
            options={
                'verbose_name': 'Кабинет',
                'verbose_name_plural': 'Кабинеты',
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram', models.URLField(blank=True, null=True, verbose_name='Instagram')),
                ('whatsapp', models.URLField(blank=True, null=True, verbose_name='WhatsApp')),
                ('telegram', models.URLField(blank=True, null=True, verbose_name='Telegram')),
                ('vk', models.URLField(blank=True, null=True, verbose_name='VK')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Phone')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255, verbose_name='Вопрос')),
                ('answer', models.TextField(verbose_name='Ответ')),
            ],
            options={
                'verbose_name': 'Часто задаваемый вопрос',
                'verbose_name_plural': 'Часто задаваемые вопросы',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=123, verbose_name='Название')),
                ('price_month', models.DecimalField(decimal_places=1, max_digits=100, verbose_name='Цена за месяц')),
                ('is_recomended', models.BooleanField(blank=True, default=False, verbose_name='РЕКОМЕНДУЕМ')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.CreateModel(
            name='SupportMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ваше ФИО')),
                ('phone', models.CharField(max_length=20, verbose_name='Ваш номер телефона')),
                ('email', models.EmailField(max_length=254, verbose_name='Ваш e-mail')),
                ('message', models.TextField(verbose_name='Ваше сообщение')),
                ('regret_to_register', models.CharField(choices=[('Компания или ИП', 'Компания или ИП'), ('Частное лицо', 'Частное лицо')], default='Компания или ИП', max_length=100, verbose_name='Оснавная цель для регистрации')),
                ('agree_to_policy', models.BooleanField(default=False, verbose_name='Я ознакомился и согласен с условиями')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Сообщение поддержки',
                'verbose_name_plural': 'Сообщения поддержки',
            },
        ),
        migrations.CreateModel(
            name='Upping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=1, max_digits=100)),
            ],
            options={
                'verbose_name': 'Поднятие в топ',
                'verbose_name_plural': 'Поднятии в топ',
            },
        ),
        migrations.CreateModel(
            name='ViewsCountProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('quest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views_count', to='user_cabinet.cabinet')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')),
                ('total', models.IntegerField(blank=True, default=0, verbose_name='Итого')),
                ('description', models.TextField(verbose_name='Описание')),
                ('pg_payment_id', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='ID платежа')),
                ('status', models.CharField(default='pending', max_length=50, verbose_name='Статус')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='user_cabinet.cabinet', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SiteOpenCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('quest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sites_count', to='user_cabinet.cabinet')),
            ],
        ),
        migrations.CreateModel(
            name='PackageStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=1, max_digits=100, verbose_name='Цена')),
                ('quantity_products', models.PositiveIntegerField(verbose_name='Количество объявлений')),
                ('quantity_tenders', models.PositiveIntegerField(verbose_name='Количество закупок')),
                ('image', models.FileField(blank=True, default='1', upload_to='images/packages/', verbose_name='Изображение')),
                ('is_advertise', models.BooleanField(blank=True, default=False, verbose_name='Просмотр сайта без рекламы')),
                ('is_contact_prov', models.BooleanField(blank=True, default=False, verbose_name='Просмотр контактов поставщиков')),
                ('is_email', models.BooleanField(blank=True, default=False, verbose_name='Показ Вашего E-mail и ссылки на ваш сайт / соцсети')),
                ('dayly_message', models.PositiveIntegerField(blank=True, default=30, verbose_name='Исходящих сообщений в день')),
                ('is_publish_phone', models.BooleanField(blank=True, default=False, verbose_name='Показ Вашего телефона незарегистрированным посетителям')),
                ('months', models.PositiveIntegerField(verbose_name='Количество месяцев')),
                ('priorety', models.PositiveIntegerField(blank=True, default=1)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packagestatuses', to='user_cabinet.status', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Статус пользователя',
                'verbose_name_plural': 'Статусы пользователей',
            },
        ),
        migrations.CreateModel(
            name='OpenNumberCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('quest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numbers_count', to='user_cabinet.cabinet')),
            ],
        ),
        migrations.AddField(
            model_name='activeuserstatus',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='active_statues', to='user_cabinet.packagestatus', verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='activeupping',
            name='upping',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_cabinet.upping'),
        ),
    ]

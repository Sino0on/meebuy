from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        (_('provider'), _('Поставщик')),
        (_('buyer'), _('Покупатель')),
    ]
    
    phone = models.CharField(max_length=20, null=True, unique=True, verbose_name=_('Номер телефона'), blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=False, max_length=250, blank=True, null=True, verbose_name=_('Имя пользователя'))
    auth_provider = models.BooleanField(default=True, verbose_name=_('Провайдер'))
    avatar = models.ImageField(blank=True, null=True, upload_to="avatars/%Y/%m",
                               verbose_name=_('Аватар'))
    is_confirm = models.BooleanField(default=False, blank=True, verbose_name=_('Подтверждение почты'))
    position = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Должность'))
    user_type = models.CharField(max_length=20, verbose_name=_('Тип пользователя'))
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

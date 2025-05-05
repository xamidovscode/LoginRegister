from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from helper.choice import *
from rest_framework_simplejwt.tokens import RefreshToken


phone_validator = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqami +998 bilan boshlanib, jami 13 ta raqamdan iborat bo‘lishi kerak (masalan: +998901234567)"
)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):

        if not phone:
            raise ValueError('Phone is required')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractUser):

    STATUS_CHOICES = [
        (NEW, "New"),
        (ACTIVE, "Active")
    ]

    ROLE_CHOICES = [
        ('student', "Student"),
        ('teacher', "Teacher"),
        ('admin', "Admin")
    ]

    username = None
    first_name = None
    last_name = None
    email = None

    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default="student")
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=NEW)
    phone = models.CharField(
        max_length=255,
        validators=[phone_validator],
        unique=True
    )
    full_name = models.CharField(max_length=255, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):

        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)

        super().save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }


class CodeVerification(BaseModel):
    code = models.CharField(
        max_length=255
    )
    user = models.ForeignKey(
        CustomUser, related_name="code_verifies", on_delete=models.CASCADE
    )
    expire_date = models.DateTimeField() # kod amal qilish vaqti



from django.contrib.auth.models import AbstractUser
from django.db import models


# Користувач з аватаром і номером телефону.
class User(AbstractUser):
    image = models.ImageField(
        upload_to="users_images", blank=True, null=True, verbose_name="Аватар"
    )
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    # Задає назву таблиці та підписи моделі в адмінці.
    class Meta:
        db_table = "user"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    # Повертає ім'я користувача.
    def __str__(self):
        return self.username

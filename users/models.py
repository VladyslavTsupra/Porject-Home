from django.contrib.auth.models import AbstractUser
from django.db import models


# User with an avatar and a phone number.
class User(AbstractUser):
    image = models.ImageField(
        upload_to="users_images", blank=True, null=True, verbose_name="Avatar"
    )
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    # Sets the table name and the model labels in the admin.
    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    # Returns the username.
    def __str__(self):
        return self.username

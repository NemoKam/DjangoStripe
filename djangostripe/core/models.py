"""
Базовые модели.
"""

import os
import uuid
import logging


from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    """
    Базовая абстрактная модель.
    """

    id = models.UUIDField(verbose_name="ID", primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.id)


class User(AbstractUser, BaseModel):
    """
    Пользователь
    """

    class Meta(BaseModel.Meta):
        db_table = "core_user"
        ordering = ["username"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    username_field = "username"

    def __str__(self):
        return self.username

    @staticmethod
    def create_admin():
        """
        Создание базового администратора.
        """
        logger = logging.getLogger("root")

        if User.objects.filter(is_staff=True, is_active=True).exists():
            logger.info("Создание пользователя-администратора... Skipped")
            return

        username = os.getenv("ADMIN_USERNAME")
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        if username and email and password:
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            logger.info("Создание пользователя-администратора... OK")
        else:
            logger.info("Создание пользователя-администратора... Skipped")

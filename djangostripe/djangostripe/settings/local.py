"""
Настройки для локального отладочного запуска.
"""

from djangostripe.settings.base import * # pylint: disable=W0401,W0614

# Игнорируем ошибку повтора строчек кода, так как локальные заупски и dev запуски - разное.
# pylint: disable=R0801
DEBUG = True

# База данных Postgresql для отладки сервиса
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    },
}

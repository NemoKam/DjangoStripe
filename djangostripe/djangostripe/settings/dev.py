"""
Настройки для запуска на тестовом стенде.
"""

from djangostripe.settings.base import * # pylint: disable=W0401,W0614

DEBUG = True

# Рабочая база Postgres
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

if os.getenv("LOGFILE"):
    LOGGING["handlers"]["logfile"] = {
        "level": "INFO",
        "class": "logging.handlers.TimedRotatingFileHandler",
        "filename": os.getenv("LOGFILE"),
        "formatter": "default",
        "when": "W0",
        "backupCount": 300,
    }
    LOGGING["loggers"]["default"]["handlers"] += ["logfile"]
    LOGGING["root"]["handlers"] += ["logfile"]

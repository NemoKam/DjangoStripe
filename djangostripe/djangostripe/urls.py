"""
Все страницы приложения.
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include


urlpatterns = [
    # Встроенная админка Django
    path("admin/", admin.site.urls),
    # Страницы для работы с товаром
    path("items/", include("items.urls")),
    # Страницы для формирования платежей
    path("buy/", include("buy.urls")),
]

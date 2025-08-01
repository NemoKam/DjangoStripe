#! /usr/bin/env bash

# Удалить старые статические файлы
rm -rf static/* && \
    # Создать или обновить структуру базы при необходимости
    python manage.py migrate && \
    # Обновить статические файлы
    python manage.py collectstatic --no-input && \
    # Инициализировать данные
    python manage.py initialize

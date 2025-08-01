"""
Инициализация приложения.
"""
from django.core.management.base import BaseCommand


from fixtures.services import get_fixture_service


class Command(BaseCommand):
    """
    Выполнение функций для инициализации приложения.
    """
    def handle(self, *args, **options):
        service = get_fixture_service()
        service.initialize()

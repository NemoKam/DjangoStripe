"""
Сервис Фикстур для заполнения базы данных необходимыми данными.
"""
from functools import lru_cache


from core.models import User


class FixtureService:
    """Объект отвечающий за начальную инициализацию системы"""

    def initialize(self) -> None:
        """Инициализация данных при первом запуске системы

        Создает пользователя-администратора, если в системе нет ни одного
        администратора и заданы переменные окружения с именем и паролем
        для создаваемого администратора.

        """
        User.create_admin()


@lru_cache
def get_fixture_service() -> FixtureService: # pylint: disable=C0116
    return FixtureService()

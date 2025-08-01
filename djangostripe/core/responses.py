"""
Модуль формата базовых ответов.
"""

from typing import Any


from rest_framework.response import Response


class BaseResponse(Response):
    """
    Базовый ответ на запрос.
    """

    def __init__(
        self,
        data: dict[str, Any] | None = None,
        status: int = 200,
        error: str | None = None,
        **kwargs
    ):
        """_summary_

        Args:
            data (dict[str, Any] | None, optional): Data. Defaults to None.
            status (int, optional): Status. Defaults to 200.
            error (str | None, optional): Error messages. Defaults to None.
        """
        # Формируем структуру ответа
        response_data: dict[str, Any] = {"error": error, "content": data}
        super().__init__(data=response_data, status=status, **kwargs)

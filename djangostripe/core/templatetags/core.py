"""
Базовые теги.
"""
from django import template


register = template.Library()


def format_number(num: float):
    """Вывод числа с пробелом в качестве разделителя тысячных разрядов"""

    num_str = f"{num:.2f}"

    integer_part, fractional_part = num_str.split(".")

    integer_part_with_spaces = " ".join(
        [
            integer_part[max(i - 3, 0) : i]
            for i in range(len(integer_part), -1, -3)
            if i != max(i - 3, 0)  # Убираем пустоты
        ][::-1]
    )

    return f"{integer_part_with_spaces}.{fractional_part}"


register.filter("format_number", format_number)

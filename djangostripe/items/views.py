"""
Страницы связанные с товарами.
"""

from django.views.generic.detail import DetailView


from items.models import Item, Order


class ItemView(DetailView):
    """
    Страница товара
    """

    template_name = "items/item_detail.html"
    model = Item


class OrderView(DetailView):
    """
    Страницы заказа
    """

    template_name = "items/order_detail.html"
    model = Order

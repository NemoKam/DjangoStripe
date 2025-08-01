"""
URL страниц товаров
"""

from django.urls import path

from items.views import OrderView

app_name = "items"


urlpatterns = [
    # Страница заказа
    path("order/<uuid:pk>/", OrderView.as_view(), name="order"),
]

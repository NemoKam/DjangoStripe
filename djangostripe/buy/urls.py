"""
URL страниц для формировании платежей
"""

from django.urls import path

from buy.views import BuyOrderByStripeView

app_name = "buy"


urlpatterns = [
    # Ссылка для оплаты товаров
    path("<uuid:pk>/", BuyOrderByStripeView.as_view(), name="buy_order"),
]

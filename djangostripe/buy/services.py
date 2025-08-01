"""
Модуль платежных сервисов.
"""
from functools import lru_cache


from django.conf import settings

import stripe


from items.models import Order


class StripeService:
    """
    Сервис для работы с платежной системой Stripe.
    """
    stripe.api_key = settings.STRIPE_API_KEY

    def get_order_stripe_payment_intent_client_secret(self, order: Order) -> str | None:
        """Функция получения client_secret по заказу для платежной системы Stripe.

        Args:
            order (Order): Заказ.

        Returns:
            str | None: client_secret.
        """

        if order.items.count() == 0:
            return None

        amount = int(order.price_after_tax * 100)

        stripe_payment_intent: stripe.PaymentIntent = stripe.PaymentIntent.create(
            amount=amount,
            currency=order.currency,
            payment_method="pm_card_visa",
        )

        return stripe_payment_intent.client_secret


@lru_cache
def get_stripe_service() -> StripeService: # pylint: disable=C0116
    return StripeService()

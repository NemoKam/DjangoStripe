"""
API для создания платежа заказа
"""

import uuid

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status


from items.models import Order

from core.responses import BaseResponse

from buy.services import get_stripe_service
from buy.serializers import StripeClientSecretSerializer


class BuyOrderByStripeView(APIView):
    """
    Обработчик для создания платежа для заказов.
    """

    def get(self, request: Request, pk: uuid.UUID):
        """
        Получение client_secret платежной системы Stripe для оплаты товаров по ID заказа.
        """

        order: Order = get_object_or_404(Order, pk=pk)

        client_secret: str | None = (
            get_stripe_service().get_order_stripe_payment_intent_client_secret(order)
        )

        if client_secret is None:
            return BaseResponse(
                status=status.HTTP_424_FAILED_DEPENDENCY,
                error="Возникла ошибка при генерации client_secret сервиса Stripe",
            )

        stripe_client_secret_serializer = StripeClientSecretSerializer(
            data={"client_secret": client_secret}
        )

        if stripe_client_secret_serializer.is_valid():
            return BaseResponse(
                data=stripe_client_secret_serializer.validated_data, status=200
            )

        return BaseResponse(
            status=status.HTTP_424_FAILED_DEPENDENCY,
            error="Возникла ошибка при валидации ответа",
        )

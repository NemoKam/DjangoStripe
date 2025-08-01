"""
Сериализаторы платежных систем.
"""

from rest_framework import serializers


class StripeClientSecretSerializer(serializers.Serializer): # pylint: disable=W0223
    """
    Сериализатор для Client Secret Payment Intent платежки Stripe.
    """

    # client_secret Stripe
    client_secret = serializers.CharField()

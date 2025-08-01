"""
Базовые сериализаторы.
"""
from rest_framework import serializers


class BaseJSONResponseSerializer(serializers.Serializer): # pylint: disable=W0223
    """
    Базовый сериализатор для ответов в формате JSON.
    """

    # error
    error = serializers.CharField(read_only=True, null=True)

    # content
    content = serializers.JSONField(read_only=True, null=True)

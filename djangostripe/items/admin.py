"""
Настройки
"""

from django.contrib import admin


from items.models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Настройки встроенной админки Django для управления товарами
    """

    list_display = ("id", "name", "description", "price", "currency")
    readonly_fields = ("id",)
    search_fields = (
        "id",
        "name",
        "description",
    )

    fields = ("id", "name", "description", "price", "currency")


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """
    Настройки встроенной админки Django для управления скидками
    """

    list_display = ("id", "percents")
    readonly_fields = ("id",)
    search_fields = ("id", "percents")

    fields = ("id", "percents")


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    """
    Настройки встроенной админки Django для управления налогами
    """

    list_display = ("id", "percents")
    readonly_fields = ("id",)
    search_fields = ("id", "percents")

    fields = ("id", "percents")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Настройки встроенной админки Django для управления заказами
    """

    list_display = (
        "id",
        "price_items",
        "discount__percents",
        "price_after_discount",
        "tax__percents",
        "price_after_tax",
    )
    readonly_fields = (
        "id",
        "price_items",
        "price_after_discount",
        "price_after_tax",
    )
    search_fields = ("id",)

    fields = (
        "items",
        "price_items",
        "discount",
        "price_after_discount",
        "tax",
        "price_after_tax",
    )

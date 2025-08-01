"""
Модели товара и связанных с ним моделей.
"""
from decimal import Decimal


from django.db import models
from django.core.exceptions import ValidationError
from django.dispatch import receiver


from core.models import BaseModel


class Item(BaseModel):
    """Модель товара."""

    CURRENCY_CHOICES = (
        ("USD", "US Dollars"),
        ("RUB", "Ruble"),
    )

    class Meta(BaseModel.Meta):
        abstract = False
        ordering = ["pk"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        db_table = "items_item"

    name = models.CharField(
        verbose_name="Name", max_length=255, blank=False, null=False
    )
    description = models.CharField(
        verbose_name="Description", max_length=1024, blank=True, null=True
    )
    price = models.DecimalField(
        verbose_name="Price", max_digits=10, decimal_places=2, blank=False, null=False
    )
    currency = models.CharField(
        verbose_name="Currency", max_length=3, choices=CURRENCY_CHOICES, default="USD"
    )

    def __str__(self) -> str:
        return f"{self.name} {self.price} {self.currency}"


class Discount(BaseModel):
    """Модель скидки."""

    class Meta(BaseModel.Meta):
        abstract = False
        ordering = ["pk"]
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"
        db_table = "items_discount"

    percents = models.DecimalField(
        verbose_name="Discount percents",
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    def __str__(self):
        return f"{self.percents}%"


class Tax(BaseModel):
    """Модель налога."""

    class Meta(BaseModel.Meta):
        abstract = False
        ordering = ["pk"]
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"
        db_table = "items_tax"

    percents = models.DecimalField(
        verbose_name="Tax percents",
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    def __str__(self):
        return f"{self.percents}%"


class Order(BaseModel):
    """Модель заказа."""

    class Meta(BaseModel.Meta):
        abstract = False
        ordering = ["pk"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        db_table = "items_order"

    items = models.ManyToManyField(
        to=Item,
        verbose_name="Items",
    )

    currency = models.CharField(
        verbose_name="Currency",
        max_length=3,
        choices=Item.CURRENCY_CHOICES,
        default="USD",
    )

    price_items = models.DecimalField(
        verbose_name="Price Sum of all items",
        max_digits=10,
        decimal_places=2,
        default=Decimal(),
        blank=False,
        null=False,
    )

    discount = models.ForeignKey(
        to=Discount,
        verbose_name="Discount",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    price_after_discount = models.DecimalField(
        verbose_name="Price after Discount",
        max_digits=10,
        decimal_places=2,
        default=Decimal(),
        blank=False,
        null=False,
    )

    tax = models.ForeignKey(
        to=Tax,
        verbose_name="Tax",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    price_after_tax = models.DecimalField(
        verbose_name="Price after Tax",
        max_digits=10,
        decimal_places=2,
        default=Decimal(),
        blank=False,
        null=False,
    )

    def calculate_price_items(self):
        """
        Функция для подсчета суммы цен товаров в заказе.
        """
        price_items = Decimal()

        for item_price in self.items.values_list("price", flat=True):
            price_items += item_price

        self.price_items = price_items

    def calculate_price_after_discount(self):
        """
        Функция для посчета суммы заказа после скидки.
        ! Необходимо сначала подсчитать сумму цен товаров в заказе.
        """
        price_before_discount = self.price_items

        price_after_discount: Decimal = price_before_discount

        if self.discount:
            discount_coefficient = self.discount.percents / 100
            price_after_discount = price_before_discount * (1 - discount_coefficient)

        self.price_after_discount = price_after_discount

    def calculate_price_after_tax(self):
        """
        Функция для посчета суммы заказа после налога.
        ! Необходимо сначала подсчитать сумму заказа после скидки.
        """
        price_before_tax: Decimal = self.price_after_discount

        price_after_tax: Decimal = price_before_tax

        if self.tax:
            tax_coefficient = self.tax.percents / 100
            price_after_tax = price_before_tax * (1 + tax_coefficient)

        self.price_after_tax = price_after_tax

    def save(self, *args, **kwargs):
        # Подсчет суммы цен товаров
        self.calculate_price_items()
        # Подсчет суммы цен после скидки
        self.calculate_price_after_discount()
        # Подсчет суммы цен после налогов
        self.calculate_price_after_tax()

        super().save(*args, **kwargs)


@receiver(models.signals.m2m_changed, sender=Order.items.through)
def check_order_currency(sender, instance: Order, action, **kwargs): # pylint: disable=W0613
    """
    Функция для проверки валют добавленных товаров в заказе.
    """
    if action == "post_add":
        # Проверка на то, что цены товаров имеют одну и ту же валюту
        currencies = instance.items.order_by("currency").values_list(
            "currency",
            flat=True
        ).distinct("currency")

        if len(currencies) > 1:
            raise ValidationError("Все товары в заказе должны быть в одной валюте.")

        instance.currency = currencies[0]
        instance.save()

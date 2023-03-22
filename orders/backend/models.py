from django.contrib.auth.models import User
from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    url = models.URLField(verbose_name="Ссылка", null=True, blank=True)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Список магазинов"
        ordering = ("-name",)

    def __str__(self):
        return self.name


class Category(models.Model):
    shops = models.ManyToManyField(
        Shop, verbose_name="Магазины", related_name="categories"
    )
    name = models.CharField(max_length=50, verbose_name="Название категории товара")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("-name",)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name="Категория продукта",
        related_name="products",
        blank=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Список продуктов"
        ordering = ("-name",)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="Продукт",
        on_delete=models.CASCADE,
        blank=True,
        related_name="product_info",
    )
    shop = models.ForeignKey(
        Shop,
        verbose_name="Магазин",
        on_delete=models.CASCADE,
        blank=True,
        related_name="product_info",
    )
    name = models.CharField(max_length=50, verbose_name="Название")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.PositiveIntegerField(verbose_name="Цена")
    price_rrc = models.PositiveIntegerField(verbose_name="Рекомендуемая розничная цена")

    class Meta:
        verbose_name = "Информация о продукте"
        verbose_name_plural = "Информационный список о продуктах"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "product",
                    "shop",
                ],
                name="unique_product_info",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.product.name} @ {self.shop.name})"


class Parameter(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Имя параметра"
        verbose_name_plural = "Список имен параметров"
        ordering = ("-name",)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name="Информация о продукте",
        related_name="product_parameters",
        blank=True,
        on_delete=models.CASCADE,
    )
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        related_name="product_parameters",
        verbose_name="Параметр",
        blank=True,
    )
    value = models.CharField(verbose_name="Значение", max_length=100)

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Список параметров"
        constraints = [
            models.UniqueConstraint(
                fields=["product_info", "parameter"], name="unique_product_parameter"
            ),
        ]

    def __str__(self):
        return (
            f"{self.product_info.product.name} - {self.parameter.name} ({self.value})"
        )


class Order(models.Model):
    STATE_CHOICES = (
        ("basket", "Статус корзины"),
        ("new", "Новый"),
        ("confirmed", "Подтвержден"),
        ("assembled", "Собран"),
        ("sent", "Отправлен"),
        ("delivered", "Доставлен"),
        ("canceled", "Отменен"),
    )

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="orders",
        blank=True,
        on_delete=models.CASCADE,
    )
    dt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        verbose_name="Статус", choices=STATE_CHOICES, max_length=15
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Список заказ"
        ordering = ("-dt",)

    def __str__(self):
        return str(self.dt)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name="Заказ",
        related_name="ordered_items",
        blank=True,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Продукт",
        related_name="ordered_items",
        blank=True,
        on_delete=models.CASCADE,
    )
    shop = models.ForeignKey(
        Shop,
        verbose_name="Магазин",
        related_name="ordered_items",
        blank=True,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Заказанная позиция"
        verbose_name_plural = "Список заказанных позиций"


class Contact(models.Model):
    CONTACT_TYPES = (
        ("email", "Email"),
        ("phone", "Phone"),
        ("address", "Address"),
    )

    type = models.CharField(
        max_length=10, choices=CONTACT_TYPES, verbose_name="Тип контакта"
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="contacts",
        blank=True,
        on_delete=models.CASCADE,
    )
    value = models.CharField(verbose_name="Значение", max_length=100)

    def __str__(self):
        return f"{self.get_type_display()}: {self.value}"



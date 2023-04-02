from rest_framework import serializers
from backend.models import (
    User,
    Category,
    Shop,
    ProductInfo,
    Product,
    Parameter,
    ProductParameter,
    OrderItem,
    Order,
    Contact,
)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            "id",
            "city",
            "street",
            "house",
            "structure",
            "building",
            "apartment",
            "user",
            "phone",
        )
        read_only_fields = ("id",)
        extra_kwargs = {"user": {"write_only": True}}


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "company",
            "position",
            "contacts",
        )
        read_only_fields = ("id",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )
        read_only_fields = ("id",)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            "id",
            "name",
            "state",
        )
        read_only_fields = ("id",)


class ProductSerializer(serializers.ModelSerializer):


    class Meta:
        model = Product
        fields = (
            "name",
            "category",
        )


class ProductParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductParameter
        fields = (
            "parameter",
            "value",
        )


class ProductInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductInfo
        fields = (
            "id",
            "model",
            "product",
            "shop",
            "quantity",
            "price",
            "price_rrc",
            # "product_parameters",
        )
        read_only_fields = ("id",)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product_info",
            "product",
            "quantity",
            "order",
            "shop"
        )
        read_only_fields = ("id",)
        extra_kwargs = {"order": {"write_only": True}}



class OrderSerializer(serializers.ModelSerializer):
    total_sum = serializers.IntegerField()
    id = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = (
            "id",
            "ordered_items",
            "status",
            "dt",
            "total_sum",
           

        )
        read_only_fields = ("id",)

class ParametrSerialaizer(serializers.ModelSerializer):
    class Meta:
        model =Parameter
        fields = ('id', 'name')
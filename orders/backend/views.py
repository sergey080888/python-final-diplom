from django.shortcuts import render
from models import (
    Shop,
    Category,
    Product,
    ProductInfo,
    Parameter,
    ProductParameter,
    Order,
    OrderItem,
    Contact
)
from serializers import (
    UserSerializer,
    CategorySerializer,
    ShopSerializer,
    ProductSerializer,
    ProductParameterSerializer,
    ProductInfoSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ParametrSerialaizer,
                       )

from rest_framework.response import Response
from rest_framework.views import APIView


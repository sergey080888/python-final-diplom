from backend.signals import new_user_registered
from django.contrib.auth.password_validation import validate_password
from django.core.validators import URLValidator
from django.http import JsonResponse
from django.shortcuts import render
from requests import get
from rest_framework.exceptions import ValidationError
from yaml import load as load_yaml, Loader
from backend.models import (
    Shop,
    Category,
    Product,
    ProductInfo,
    Parameter,
    ProductParameter,
    Order,
    OrderItem,
    Contact,
    ConfirmEmailToken
)
from backend.serializers import (
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




class PartnerUpdate(APIView):
    """
    Класс для обновления прайса от поставщика
    """

    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse(
        #         {"Status": False, "Error": "Log in required"}, status=403
        #     )

        # if request.user.type != "shop":
        #     return JsonResponse(
        #         {"Status": False, "Error": "Только для магазинов"}, status=403
        #     )

        url = request.data.get("url")
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({"Status": False, "Error": str(e)})
            else:
                stream = get(url).content

                data = load_yaml(stream, Loader=Loader)

                shop, _ = Shop.objects.get_or_create(
                    name=data["shop"], user_id=request.user.id
                )
                for category in data["categories"]:
                    category_object, _ = Category.objects.get_or_create(
                        id=category["id"], name=category["name"]
                    )
                    category_object.shops.add(shop.id)
                    category_object.save()
                ProductInfo.objects.filter(shop_id=shop.id).delete()
                for item in data["goods"]:
                    product, _ = Product.objects.get_or_create(
                        name=item["name"], category_id=item["category"]
                    )

                    product_info = ProductInfo.objects.create(
                        product_id=product.id,
                        external_id=item["id"],
                        model=item["model"],
                        price=item["price"],
                        price_rrc=item["price_rrc"],
                        quantity=item["quantity"],
                        shop_id=shop.id,
                    )
                    for name, value in item["parameters"].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(
                            product_info_id=product_info.id,
                            parameter_id=parameter_object.id,
                            value=value,
                        )

                return JsonResponse({"Status": True})

        return JsonResponse(
            {"Status": False, "Errors": "Не указаны все необходимые аргументы"}
        )

class RegisterAccount(APIView):
    """
    Для регистрации покупателей
    """

    # Регистрация методом POST
    def post(self, request, *args, **kwargs):
        # проверяем обязательные аргументы
        if {
            "first_name",
            "last_name",
            "email",
            "password",
            "company",
            "position",
            }.issubset(request.data):
            errors = {}

            # проверяем пароль на сложность

            try:
                validate_password(request.data["password"])
            except Exception as password_error:
                error_array = []
                # noinspection PyTypeChecker
                for item in password_error:
                    error_array.append(item)
                return JsonResponse(
                    {"Status": False, "Errors": {"password": error_array}}
                )
            else:
                # проверяем данные для уникальности имени пользователя
                request.data._mutable = True
                request.data.update({})
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    # сохраняем пользователя
                    user = user_serializer.save()
                    user.set_password(request.data["password"])
                    user.save()
                    new_user_registered.send(sender=self.__class__, user_id=user.id)
                    return JsonResponse({"Status": True})
                else:
                    return JsonResponse(
                        {"Status": False, "Errors": user_serializer.errors}
                    )

        return JsonResponse(
            {"Status": False, "Errors": "Не указаны все необходимые аргументы"}
        )


class ConfirmAccount(APIView):
    """
    Класс для подтверждения почтового адреса
    """

    # Регистрация методом POST
    def post(self, request, *args, **kwargs):
        # проверяем обязательные аргументы
        if {"email", "token"}.issubset(request.data):
            token = ConfirmEmailToken.objects.filter(
                user__email=request.data["email"], key=request.data["token"]
            ).first()
            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()
                return JsonResponse({"Status": True})
            else:
                return JsonResponse(
                    {"Status": False, "Errors": "Неправильно указан токен или email"}
                )

        return JsonResponse(
            {"Status": False, "Errors": "Не указаны все необходимые аргументы"}
        )

from django.urls import path
from backend.views import (
    PartnerUpdate,
    RegisterAccount,
    ConfirmAccount,
    Login,
    ContactView,
    DetailsView,
    ShopsList,
    ProductView,
    BasketView,
    OrderView,
    СategoriesListView,
    PartnerState,
    PartnerOrders,
)
from django_rest_passwordreset.views import (
    reset_password_request_token,
    reset_password_confirm,
)
from rest_framework.routers import DefaultRouter

r = DefaultRouter()
r.register("partner/orders", PartnerOrders, basename="book")
app_name = "backend"
urlpatterns = [
    path("partner/update", PartnerUpdate.as_view(), name="partner-update"),
    path("register", RegisterAccount.as_view(), name="register"),
    path("register/confirm", ConfirmAccount.as_view(), name="user-register-confirm"),
    path("login", Login.as_view(), name="login"),
    path("password_reset", reset_password_request_token, name="password-reset"),
    path(
        "password_reset/confirm", reset_password_confirm, name="password-reset-confirm"
    ),
    path("contact", ContactView.as_view(), name="contact"),
    path("user/details", DetailsView.as_view(), name="detail"),
    path("shops", ShopsList.as_view(), name="shops"),
    path("products", ProductView.as_view(), name="products"),
    path("basket", BasketView.as_view(), name="basket"),
    path("order", OrderView.as_view(), name="order"),
    path("categories", СategoriesListView.as_view(), name="categories"),
    path("partner/state", PartnerState.as_view(), name="partner-state"),
] + r.urls

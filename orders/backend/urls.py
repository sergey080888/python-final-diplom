from django.urls import path
from backend.views import PartnerUpdate,RegisterAccount,ConfirmAccount,Login,ContactView,DetailsView,ShopsList
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

app_name = "backend"
urlpatterns = [path("partner/update", PartnerUpdate.as_view(), name="partner-update"),
                path("register", RegisterAccount.as_view(), name="register"),
                path("register/confirm", ConfirmAccount.as_view(), name="user-register-confirm"),
                path("login", Login.as_view(), name="login"),
                path("password_reset", reset_password_request_token, name="password-reset"),
                path("password_reset/confirm", reset_password_confirm, name="password-reset-confirm"),
                path("contact", ContactView.as_view(),name="contact"),
                path("user/details", DetailsView.as_view(),name="detail"),
                path("shops", ShopsList.as_view(),name="shops"),

    ]

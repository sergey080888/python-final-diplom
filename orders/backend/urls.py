from django.urls import path
from backend.views import PartnerUpdate,RegisterAccount,ConfirmAccount


app_name = "backend"
urlpatterns = [path("partner/update", PartnerUpdate.as_view(), name="partner-update"),
               path("register", RegisterAccount.as_view(), name="register"),
               path(
                   "register/confirm", ConfirmAccount.as_view(), name="user-register-confirm"
               ),
               # path("login", Login.as_view(), name="login"),

               ]

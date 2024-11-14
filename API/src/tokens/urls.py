from django.urls import path
from .views import ObtainTokenView, RefreshTokenView

urlpatterns = [
    path("login/", view=ObtainTokenView.as_view(), name="obtain_token"),
    path("refresh/", view=RefreshTokenView.as_view(), name="refresh_token")
]



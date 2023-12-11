from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, UserRegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "accounts"
router = routers.SimpleRouter()
router.register("user", UserViewSet)
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls

# Admin: root9876
# {
#   "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMjIwOTM4NSwiaWF0IjoxNzAyMTIyOTg1LCJqdGkiOiJhNGZlOTJiMjg2N2M0OTVjYWIzZGIzNzFiMGMwY2VmZCIsInVzZXJfaWQiOjF9.kwP6gEoUU7OIlVB2hJG2hn6b7X9H2D-4X5qEyj20m_o",
#   "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyMTIzMjg1LCJpYXQiOjE3MDIxMjI5ODUsImp0aSI6IjQ0NjZhODdkYjU4ZTQ4OWFiNTI3NWQzMDkzMDA4M2NjIiwidXNlcl9pZCI6MX0.3CKmxnKEZpkNDn-3zG9_n0YDn_zqMWSLI4FMjRSSuUc"
# }

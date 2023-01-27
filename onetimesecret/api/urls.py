from django.urls import path

from .views import SecretCreate, SecretRead

urlpatterns = [
    path("generate/", SecretCreate.as_view(), name="create_secret"),
    path("secrets/<secret_key>/", SecretRead.as_view(), name="read_secret"),
]

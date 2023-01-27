import random
import string
from datetime import datetime

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN,
                                   HTTP_404_NOT_FOUND)

from .models import TIME_OF_END, Secret
from .serializers import SecretCreateSerializer, SecretReadSerializer


def generate_secret_key(size=15, chars=string.ascii_letters + string.digits):
    """Generation random secret_key for field lifetime."""

    result = "".join(random.choice(chars) for _ in range(size))
    return result


class SecretCreate(generics.CreateAPIView):
    queryset = Secret.objects.all()
    serializer_class = SecretCreateSerializer

    def post(self, request, *args, **kwargs):
        """The function of creating a new secret."""

        serializer = SecretCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["secret_key"] = generate_secret_key()
            serializer.validated_data["time_of_end"] = TIME_OF_END[
                serializer.validated_data["lifetime"]
            ]
            serializer.save()
            msg = {
                "Passphrase": serializer.data["passphrase"],
                "Secret_key": serializer.validated_data["secret_key"]
            }
            return Response(msg, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SecretRead(generics.CreateAPIView):
    queryset = Secret.objects.all()
    serializer_class = SecretReadSerializer

    def post(self, request, *args, **kwargs):
        """The function of obtaining a secret by a passphrase."""

        try:
            secret = Secret.objects.get(
                secret_key=self.kwargs.get("secret_key")
            )
        except Secret.DoesNotExist:
            msg = {"error": "The secret not found"}
            return Response(msg, status=HTTP_404_NOT_FOUND)
        serializer = SecretReadSerializer(secret, data=request.data)
        if serializer.is_valid():
            passphrase = request.data["passphrase"]
            if secret.is_viewed is True:
                return Response({"Message": "The secret was obtained earlier"})
            if passphrase == secret.passphrase and secret.is_viewed is False:
                if datetime.now() < secret.time_of_end:
                    secret.is_viewed = True
                    serializer.save()
                    msg = {"Secret": secret.secret}
                    return Response(msg, status=HTTP_200_OK)
                msg = {"error": "The secret's retention period has expired."}
                return Response(msg, status=HTTP_403_FORBIDDEN)
            msg = {"error": "Invalid passphrase."}
            return Response(msg, status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

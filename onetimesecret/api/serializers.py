from rest_framework import serializers

from .models import TIME_CHOICE, Secret


class SecretCreateSerializer(serializers.ModelSerializer):
    lifetime = serializers.ChoiceField(choices=TIME_CHOICE, default="1")

    class Meta:
        model = Secret
        fields = ["secret", "passphrase", "lifetime"]

    def validate(self, data: list) -> list:
        secrets = self.initial_data.get("secret")
        if not secrets:
            msg = "You did not provide anything to share"
            raise serializers.ValidationError(msg)
        return data


class SecretReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ["passphrase"]

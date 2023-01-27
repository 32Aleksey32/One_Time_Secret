from django.contrib import admin

from .models import Secret


@admin.register(Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "secret",
        "passphrase",
        "is_viewed",
        "secret_key",
        "lifetime",
        "created_date",
        "time_of_end",
    )
    search_fields = ("secret",)
    list_filter = ("created_date",)
    empty_value_display = "-пусто-"

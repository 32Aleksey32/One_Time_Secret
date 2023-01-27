import datetime as dt

from django.db import models
from django_cryptography.fields import encrypt

TIME_CHOICE = (
    ("1", "7 days"),
    ("2", "3 days"),
    ("3", "1 day"),
    ("4", "1 hour"),
    ("5", "30 minutes"),
    ("6", "5 minutes"),
)

TIME_OF_END = {
    "1": (dt.datetime.now() + dt.timedelta(days=7)),
    "2": (dt.datetime.now() + dt.timedelta(days=3)),
    "3": (dt.datetime.now() + dt.timedelta(days=1)),
    "4": (dt.datetime.now() + dt.timedelta(hours=1)),
    "5": (dt.datetime.now() + dt.timedelta(minutes=30)),
    "6": (dt.datetime.now() + dt.timedelta(minutes=5)),
}


class Secret(models.Model):
    """The model creates a table and contains all the information about
     the secret and its data."""

    secret = encrypt(models.CharField(
        "Secret",
        help_text="Enter secret content",
        max_length=10000,
    ))
    passphrase = encrypt(models.CharField(
        "Passphrase",
        help_text="Using this phrase, you will be shown the secret",
        max_length=100,
    ))
    is_viewed = models.BooleanField("Already viewed", default=False)
    secret_key = models.CharField("Slug", max_length=20, unique=True)
    lifetime = models.CharField(
        verbose_name="Lifetime",
        max_length=20,
        choices=TIME_CHOICE,
        help_text="Lifetime of secret content"
    )
    time_of_end = models.DateTimeField(verbose_name="Time of end")
    created_date = models.DateTimeField("Created date", auto_now_add=True)

    class Meta:
        verbose_name = "Secret"
        verbose_name_plural = "Secrets"

    def __str__(self):
        return self.secret

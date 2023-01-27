from datetime import datetime

from onetimesecret.celery import app

from .models import Secret


@app.task
def delete_secret():
    """The function of deleting expired secrets."""

    secret = Secret.objects.filter(time_of_end__lt=datetime.now())
    secret.delete()

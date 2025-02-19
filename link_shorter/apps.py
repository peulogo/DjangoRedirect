from django.apps import AppConfig
from .rabbitmq import rabbitmq


class LinkShorterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "link_shorter"

    def ready(self):
        try:
            rabbitmq.connect()
        except Exception as e:
            print(f"Ошибка подключения к RabbitMQ: {e}")

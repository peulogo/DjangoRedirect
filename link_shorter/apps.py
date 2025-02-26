from django.apps import AppConfig
from .rabbitmq import rabbitmq
from .redis_cache import redis_cache


class LinkShorterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "link_shorter"

    def ready(self):

        try:
            rabbitmq.connect()
        except Exception as e:
            print(f"Ошибка подключения к RabbitMQ: {e}")

        try:
            redis_cache.connect()
        except Exception as e:
            print(f"Ошибка подключения к Redis: {e}")
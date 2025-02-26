from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.timezone import now
import pika
import json

from .rabbitmq import rabbitmq
from .redis_cache import redis_cache

from .models import Redirect


def get_full_url(hash: str):

    cached = redis_cache.get_url(hash)
    if cached:

        redirect_id, full_url = cached
        return redirect_id, full_url
    else:
        try:
            redirect_obj = Redirect.objects.get(hash=hash)
            full_url = redirect_obj.full_url
            redirect_id = redirect_obj.id

            redis_cache.set_url(hash, [redirect_id, full_url])

            return redirect_id, full_url
        except Redirect.DoesNotExist:
            raise KeyError('Попробуй другой URL. URL не найден в базе данных')

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def send_to_rabbitmq(message: dict):
    rabbitmq.send_message(message)


def redirection(request, hash):
    try:
        redirect_id, full_url = get_full_url(hash)

        client_ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")
        message = {
            "short_url_id": redirect_id,
            "user_agent": user_agent,
            "ip_address": client_ip,
            "created_at": now().isoformat()
        }

        send_to_rabbitmq(message)
        return redirect(full_url)

    except KeyError as e:
        return HttpResponse(e.args[0], status=404)




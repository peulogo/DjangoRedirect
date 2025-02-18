from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.timezone import now
import pika
import json
from .models import Redirect


def get_full_url(url: str) -> str:
    try:
        redirect_obj = Redirect.objects.get(hash=url)
    except Redirect.DoesNotExist:
        raise KeyError('Try another url. No such urls in DB')
    return redirect_obj.full_url


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def send_to_rabbitmq(message: dict):
    credentials = pika.PlainCredentials('rmuser', 'rmpassword')
    parameters = pika.ConnectionParameters(host="rabbitmq", credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange="statistic_service", exchange_type="direct", durable=True)

    channel.basic_publish(
        exchange="statistic_service",
        routing_key="click.log",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    connection.close()


def redirection(request, hash):

    try:
        redirect_obj = get_object_or_404(Redirect, hash=hash)
        full_link = redirect_obj.full_url

        client_ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")
        base_url = request.build_absolute_uri('/')[:-1]
        message = {
            "short_url": f"{base_url}/{hash}",
            "user_agent": user_agent,
            "ip_address": client_ip,
        }

        send_to_rabbitmq(message)
        return redirect(full_link)

    except KeyError as e:
        return HttpResponse(e.args[0], status=404)




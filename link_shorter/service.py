from django.http import HttpResponse
from django.shortcuts import redirect

from .models import Redirect


def get_full_url(url: str) -> str:
    try:
        redirect_obj = Redirect.objects.get(hash=url)
    except Redirect.DoesNotExist:
        raise KeyError('Try another url. No such urls in DB')
    return redirect_obj.full_url


def redirection(request, hash):
    try:
        full_link = get_full_url(hash)
        return redirect(full_link)
    except KeyError as e:
        return HttpResponse(e.args[0], status=404)




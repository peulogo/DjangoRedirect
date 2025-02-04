from django.contrib import admin
from django.urls import path

from . import service
from .views import RedirectAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/short', RedirectAPIView.as_view()),
    path('api/v1/short', RedirectAPIView.as_view(), name='short-url'),
    path('<str:hash>/', service.redirection)
]

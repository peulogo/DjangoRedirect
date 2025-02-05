import random
from urllib.parse import urlparse
from django.db import models
from django.conf import settings

class Redirect(models.Model):

    hash = models.CharField(max_length=6, unique=True)
    full_url = models.CharField(max_length=1000, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hash

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.hash:

            while True:
                self.hash = ''.join(
                    random.choices(
                        settings.CHARACTERS,
                        k=settings.TOKEN_LENGTH
                    )
                )
                if not Redirect.objects.filter(
                    hash=self.hash
                ).exists():
                    break

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)



class ClickLog(models.Model):

    short_url = models.ForeignKey(Redirect, on_delete=models.CASCADE, related_name="click_logs")
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    clicked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Click on {self.short_url.hash} at {self.clicked_at}"
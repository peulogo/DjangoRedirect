import random
from urllib.parse import urlparse
from django.db import models
from django.conf import settings

class Redirect(models.Model):

    id = models.AutoField(primary_key=True)
    hash = models.CharField(max_length=6, unique=True)
    full_url = models.CharField(max_length=1000, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hash

    class Meta:
        db_table = "short_urls"
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
    id = models.AutoField(primary_key=True)
    short_url_id = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "click_log"
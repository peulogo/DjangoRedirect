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
            parsed_url = urlparse(self.full_url)
            self.hash = parsed_url.path.lstrip('/')

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

    def __str__(self) -> str:
        return f'{self.hash} -> {self.full_url}'
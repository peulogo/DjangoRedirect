from django.contrib import admin
from .models import Redirect

@admin.register(Redirect)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'hash',
        'full_url',
        'created_at',
    )
    search_fields = ('hash',)
    ordering = ('-created_at',)
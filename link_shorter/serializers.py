from rest_framework import serializers, status

from .models import Redirect


class TokenSerializer(serializers.ModelSerializer):

    url = serializers.URLField(source="full_url")

    class Meta:
        model = Redirect
        fields = ('url',)
        extra_kwargs = {'url': {'validators': []}}

    def create(self, validated_data):
        full_url = validated_data['full_url']
        token, created = Redirect.objects.get_or_create(full_url=full_url)
        if created:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK
        return token, status_code
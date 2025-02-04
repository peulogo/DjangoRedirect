from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Redirect
from .serializers import TokenSerializer


class RedirectAPIView(APIView):

    def post(self, request):
        base_url = request.build_absolute_uri('/')[:-1]
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            full_url = request.data['url']

            redirect_obj = Redirect(full_url=full_url)
            redirect_obj.save()

            short_url = f"{base_url}/{redirect_obj.hash}"
            response_data = {
                "data": {
                    "url": short_url
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=400)

    def get(self, request):
        short_url = request.query_params.get("url", None)

        if not short_url:
            return Response({"error": "URL parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        hash_part = short_url.rstrip("/").split("/")[-1]

        redirect_obj = get_object_or_404(Redirect, hash=hash_part)
        return Response({"full_url": redirect_obj.full_url}, status=status.HTTP_200_OK)

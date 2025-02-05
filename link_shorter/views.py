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

            hash_value, status_code = serializer.create(
                validated_data=serializer.validated_data
            )

            short_url = f"{base_url}/{hash_value.hash}"
            response_data = {
                "data": {
                    "url": short_url,
                }
            }
            return Response(response_data, status=status_code)
        return Response({"error": serializer.errors}, status=400)

    def patch(self, request, *args, **kwargs):
        hash_value = kwargs.get("hash")
        if not hash_value:
            return Response({"error": "Hash parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        redirect_obj = get_object_or_404(Redirect, hash=hash_value)
        new_url = request.data.get("url")

        if not new_url:
            return Response({"error": "New URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        redirect_obj.full_url = new_url
        redirect_obj.save()

        return Response({"message": "URL updated successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        hash_value = kwargs.get("hash")

        if not hash:
            return Response({"error": "URL parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        redirect_obj = get_object_or_404(Redirect, hash=hash_value)
        redirect_obj.delete()

        return Response({"message": "URL deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

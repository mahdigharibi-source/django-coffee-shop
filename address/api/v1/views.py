
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AddressCreateSerializer
class AddressCreateApiView(APIView):
    serializer_class = AddressCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
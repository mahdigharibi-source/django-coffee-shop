from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AddressCreateSerializer, AddressUpdateSerializer
from ...models import Address


class AddressCreateApiView(APIView):
    serializer_class = AddressCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class AddressUpdateApiView(APIView):
    serializer_class = AddressUpdateSerializer

    def get(self, request, *args, **kwargs):
        address = get_object_or_404(Address, user=request.user, pk=kwargs['pk'])
        serializer = self.serializer_class(instance=address)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        address = get_object_or_404(Address, user=request.user, pk=kwargs['pk'])
        serializer = self.serializer_class(instance=address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        address = get_object_or_404(Address, user=request.user, pk=kwargs['pk'])
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import serializers

from address.models import Address


class AddressCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ('created_at','updated_at')

        extra_kwargs = {'user':{'read_only':True}}

class AddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('created_at', 'updated_at')
        extra_kwargs = {'user': {'read_only': True}}

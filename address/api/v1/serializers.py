from rest_framework import serializers

from address.models import Address


class AddressCreateSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Address
        exclude = ('user','created_at','updated_at')
        extra_kwargs = {'user': {'read_only': True}}

    def get_user_info(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'phone_number': obj.user.profile.phone_number,
        }

class AddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('created_at', 'updated_at')
        extra_kwargs = {'user': {'read_only': True}}

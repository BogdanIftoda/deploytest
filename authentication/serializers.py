from rest_framework import serializers

from authentication.models import User, Address


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="get_role_display", read_only=True)
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "email", "role", "phone_number", "address")

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.role = validated_data.get("role", instance.role)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)

        address_data = validated_data.pop("address", None)

        if address_data:
            address = instance.address
            if address is None:
                address = Address.objects.create(**address_data)
                instance.address = address
            else:
                for key, value in address_data.items():
                    setattr(address, key, value)
            address.save()
        instance.save()
        return instance

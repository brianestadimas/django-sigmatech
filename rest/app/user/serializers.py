from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest.app.user.models import User
from rest.app.payment.models import Transaction


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'address', 'created_at')


class TopupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'balance_before', 'balance_after', 'created_at')

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'balance_before', 'balance_after', 'created_at', 'remarks', 'target_user', 
            'transaction_type', 'payment_type')

class PaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'balance_before', 'balance_after', 'created_at', 'remarks')

class TransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'balance_before', 'balance_after', 'created_at', 'remarks', 'target_user')

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone_number', 'pin', 'first_name', 'last_name', 'address')
        extra_kwargs = {'pin': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):

    phone_number = serializers.CharField(max_length=255)
    pin = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number", None)
        pin = data.get("pin", None)
        user = User.objects.get(phone_number=phone_number, pin=pin)
        if user is None:
            raise serializers.ValidationError(
                'A user with this phone_number and pin is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given phone_number and pin does not exists'
            )
        return {
            'phone_number':user.phone_number,
            'token': jwt_token,
        }

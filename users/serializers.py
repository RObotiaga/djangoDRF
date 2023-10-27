from rest_framework import serializers

from courses.serializers import PaymentSerializer
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = CustomUser
        fields = '__all__'


class UserSerializerForOthers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('avatar',)

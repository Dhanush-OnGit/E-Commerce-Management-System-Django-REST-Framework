
from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email","role"]
        read_only_fields = ["id", "role"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

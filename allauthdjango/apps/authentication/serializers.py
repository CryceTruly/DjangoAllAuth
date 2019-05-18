from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        error_messages={
            "min_length": "Password should be atleast {min_length} characters"
        }
    )
    token = serializers.CharField(max_length=256, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

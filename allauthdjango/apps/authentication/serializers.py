from rest_framework import serializers
from .models import User
from allauthdjango.apps.authentication.social_validation import SocialValidation


class LinkedInSerializer(serializers.Serializer):
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

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class GoogleAuthSerializer(serializers.ModelSerializer):
    """
    Handle serialization and deserialization of User objects
    """

    access_token = serializers.CharField()

    class Meta:
        model = User
        fields = ['access_token']

    @staticmethod
    def validate_access_token(access_token):
        """
        Handles validating a request and decoding and getting user's info
        associated to an account on Google then authenticates the User
        : params access_token:
        : rturn: user_token
        """

        id_info = SocialValidation.google_auth_validation(
            access_token=access_token)

        # check if data data retrieved once token decoded is empty
        if id_info is None:
            raise serializers.ValidationError('token is not valid')

        # check if a user exists after decoding the token in the payload
        # the user_id confirms user existence since its a unique identifier

        user_id = id_info['sub']

        # query database to check if a user with the same email exists
        user = User.objects.filter(email=id_info.get('email'))

        # if the user exists,return the user token
        if user:
            return user[0].token

        # create a new user if no new user exists
        first_and_second_name = id_info.get('name').split()
        first_name = first_and_second_name[0]
        second_name = first_and_second_name[1]
        payload = {
            'email': id_info.get('email'),
            'first_name': first_name,
            'last_name': second_name,
            'password': "XXXXXXXXA!S!"
        }

        new_user = User.objects.create_user(**payload)
        new_user.is_verified = True
        new_user.social_id = user_id
        new_user.save()

        return new_user.token

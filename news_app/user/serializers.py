from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for custom User object"""

    class Meta:
        model = User
        fields = ("email", "password", "name")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
                "help_text": "Please enter valid password:",
            }
        }

    def validate_password(self, data):
        """Password validation for User object"""
        password = data
        errors = dict()
        try:
            validate_password(password=password, user=User)
        except ValidationError as e:
            errors["password"] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors["password"])
        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and returns it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer fot the authenticate user"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """validate an authenticated user"""
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )

        if not user:
            msg = "Unable to authenticate with provided credentials"
            raise serializers.ValidationError(msg, code="authentication")

        attrs["user"] = user
        return attrs

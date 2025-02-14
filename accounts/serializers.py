from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'role', 'profile_picture', 'bio', 'created_at', 'updated_at', 'last_login']
        extra_kwargs = {
            'email': {'read_only': True},
            'phone': {'read_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'profile_picture': {'required': False},
            'bio': {'required': False},
        }

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("New password cannot be the same as the old password")
        return data
    

from rest_framework import serializers
from accounts.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()  # ✅ Ensures full URL

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'role',
            'profile_picture',
            'bio',
        )

    def get_profile_picture(self, obj):
        """Ensures `profile_picture` returns a full URL instead of a relative path."""
        request = self.context.get("request")  # ✅ Get request context
        if obj.profile_picture:
            return request.build_absolute_uri(obj.profile_picture.url) if request else obj.profile_picture.url
        return None  # ✅ If no profile picture, return `None`

from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


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



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.is_verified:
            raise serializers.ValidationError("Email not verified. Please verify your email.")

        return {'user': user}



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("New password cannot be the same as the old password")
        return data
    

class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

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
        request = self.context.get("request")
        if obj.profile_picture:
            return request.build_absolute_uri(obj.profile_picture.url) if request else obj.profile_picture.url
        return None
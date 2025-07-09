from rest_framework import serializers
from .models import Leave, UserProfile, Attendance,Department
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import jwt
from django.contrib.auth.hashers import check_password
class RegisterSerializer(serializers.ModelSerializer):
    # Extra fields from UserProfile
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    position = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    salary = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'position', 'phone_number', 'salary', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        role = validated_data.pop('role')
        position = validated_data.pop('position', '')
        phone_number = validated_data.pop('phone_number', '')
        salary = validated_data.pop('salary', None)
        is_active = validated_data.pop('is_active', True)

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Update UserProfile
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'role': role,
                'position': position,
                'phone_number': phone_number,
                'salary': salary,
                'is_active': is_active
            }
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        # Generate JWT tokens using SimpleJWT
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        profile = user.userprofile

        return {
            "refresh": str(refresh),
            "access": str(access),
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": profile.role,
            "position": profile.position,
            "phone_number": profile.phone_number,
            "salary": str(profile.salary) if profile.salary else None,
            "is_active": profile.is_active
        }

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)

    class Meta:
        model = UserProfile
        fields = ['department', 'first_name', 'last_name', 'phone_number', 'position']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        # Update built-in User model fields
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update UserProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = UserProfile
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone_number', 'position', 'role'
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'date', 'check_in_time']
        read_only_fields = ['date', 'check_in_time']

class LeaveApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = "__all__"

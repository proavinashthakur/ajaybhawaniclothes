# django
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_str
from django.contrib.auth import authenticate

# rest framework
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import ValidationError, PermissionDenied


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password', 'phone')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': True},
        }


    def create(self, validated_data):
        instance = get_user_model().objects.create_user(**validated_data)
        return instance





class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=64, write_only=True
    )
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = get_user_model().objects.get(email=obj.email)

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'tokens'
        )
        read_only_fields = ('first_name', 'last_name')

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)

        if not user:
            raise PermissionDenied({"detail": 'Invalid credentials, try again.'})
        if not user.is_active:
            raise PermissionDenied({"detail": 'Account disabled.'})
        if not user.is_verified:
            raise PermissionDenied({"detail": 'Email is not verified yet.'})

        return user


class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {'invalid_token': 'Token is expired or invalid.'}

    def save(self, **kwargs):
        try:
            RefreshToken(self.validated_data['refresh_token']).blacklist()
        except TokenError:
            raise ValidationError({'detail': 'Token is expired or invalid.'})



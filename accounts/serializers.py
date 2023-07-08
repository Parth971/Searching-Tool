from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer

from accounts.constants import (
    INVALID_EMAIL, INCORRECT_OLD_PASSWORD, PASSWORD_HELP_TEXT,
    PASSWORD_MISMATCH, EMAIL_NOT_ACTIVATED, EMAIL_ALREADY_ACTIVATED, EMAIL_NOT_UNIQUE, EMAIL_REQUIRED_ERROR,
    PASSWORD_REQUIRED_ERROR, FIRST_NAME_REQUIRED_ERROR, LAST_NAME_REQUIRED_ERROR, MOBILE_NUMBER_REQUIRED_ERROR,
    COMPANY_NAME_REQUIRED_ERROR, JOB_TITLE_REQUIRED_ERROR, LOGIN_FAILED,
    PROFILE_PIC_REQUIRED_ERROR
)
from accounts.models import User
from accounts.utils import send_email_verification_email
from accounts.validators import validate_password, validate_first_name, validate_last_name, validate_mobile_number


class LoginSerializer(TokenObtainPairSerializer, TokenObtainSerializer):
    default_error_messages = {"no_active_account": LOGIN_FAILED}

    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        return token

    def validate(self, attrs):
        user = User.get_object(query={'email': attrs[self.username_field]})

        if user and not user.is_active:
            raise serializers.ValidationError({'email': 'Email is not verified'})

        return super().validate(attrs)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message=EMAIL_NOT_UNIQUE)],
        error_messages={'required': EMAIL_REQUIRED_ERROR, 'blank': EMAIL_REQUIRED_ERROR}
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text=PASSWORD_HELP_TEXT,
        validators=[validate_password],
        error_messages={'required': PASSWORD_REQUIRED_ERROR, 'blank': PASSWORD_REQUIRED_ERROR}
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'job_title', 'company_name', 'mobile_number')
        extra_kwargs = {
            'first_name': {
                'required': True,
                'allow_blank': False,
                'validators': [validate_first_name],
                'error_messages': {
                    'required': FIRST_NAME_REQUIRED_ERROR,
                    'blank': FIRST_NAME_REQUIRED_ERROR
                }
            },
            'last_name': {
                'required': True,
                'allow_blank': False,
                'validators': [validate_last_name],
                'error_messages': {
                    'required': LAST_NAME_REQUIRED_ERROR,
                    'blank': LAST_NAME_REQUIRED_ERROR
                }
            },
            'mobile_number': {
                'validators': [validate_mobile_number],
                'error_messages': {
                    'required': MOBILE_NUMBER_REQUIRED_ERROR,
                    'blank': MOBILE_NUMBER_REQUIRED_ERROR
                }
            },
            'job_title': {
                'error_messages': {
                    'required': JOB_TITLE_REQUIRED_ERROR,
                    'blank': JOB_TITLE_REQUIRED_ERROR
                }
            },
            'company_name': {
                'error_messages': {
                    'required': COMPANY_NAME_REQUIRED_ERROR,
                    'blank': COMPANY_NAME_REQUIRED_ERROR
                }
            }
        }

    def create(self, validated_data):
        """
        This function will create user instance and send email regarding email verification.
        :rtype: User object
        """
        user = User.objects.create_user(**validated_data, is_active=False)
        send_email_verification_email(user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'job_title', 'company_name', 'mobile_number')
        extra_kwargs = {
            'first_name': {
                'required': True,
                'allow_blank': False,
                'validators': [validate_first_name],
                'error_messages': {
                    'required': FIRST_NAME_REQUIRED_ERROR,
                    'blank': FIRST_NAME_REQUIRED_ERROR
                }
            },
            'last_name': {
                'required': True,
                'allow_blank': False,
                'validators': [validate_last_name],
                'error_messages': {
                    'required': LAST_NAME_REQUIRED_ERROR,
                    'blank': LAST_NAME_REQUIRED_ERROR
                }
            },
            'mobile_number': {
                'validators': [validate_mobile_number],
                'error_messages': {
                    'required': MOBILE_NUMBER_REQUIRED_ERROR,
                    'blank': MOBILE_NUMBER_REQUIRED_ERROR
                }
            },
            'job_title': {
                'error_messages': {
                    'required': JOB_TITLE_REQUIRED_ERROR,
                    'blank': JOB_TITLE_REQUIRED_ERROR
                }
            },
            'company_name': {
                'error_messages': {
                    'required': COMPANY_NAME_REQUIRED_ERROR,
                    'blank': COMPANY_NAME_REQUIRED_ERROR
                }
            },
            'email': {'read_only': True},
        }


class ProfilePicSerializer(serializers.ModelSerializer):
    profile_pic = Base64ImageField(required=True, allow_null=False, allow_empty_file=False, error_messages={
        'required': PROFILE_PIC_REQUIRED_ERROR,
        'blank': PROFILE_PIC_REQUIRED_ERROR
    })

    class Meta:
        model = User
        fields = ('profile_pic',)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={
        'required': EMAIL_REQUIRED_ERROR,
        'blank': EMAIL_REQUIRED_ERROR,
    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        """
        This function will check if user exists for given email field, if not raise Validation error.
        :rtype: dict
        """
        email = attrs.get('email')
        self.user = User.get_object(query={'email': email})
        if not self.user:
            raise serializers.ValidationError({'email': INVALID_EMAIL})

        return attrs


class ResendVerifyEmailSerializer(EmailSerializer):
    def validate(self, attrs):
        """
        This function will check if user should not be active, if user already active it will raise Validation error.
        :rtype: dict
        """
        attrs = super().validate(attrs)
        if self.user and self.user.is_active:
            raise serializers.ValidationError({'email': EMAIL_ALREADY_ACTIVATED})
        return attrs


class ForgotPasswordSerializer(EmailSerializer):
    def validate(self, attrs):
        """
        This function will check if user is active, if user not active it will raise Validation error.
        :rtype: dict
        """
        attrs = super().validate(attrs)
        if self.user and not self.user.is_active:
            raise serializers.ValidationError({'email': EMAIL_NOT_ACTIVATED})
        return attrs


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        error_messages={
            'required': PASSWORD_REQUIRED_ERROR,
            'blank': PASSWORD_REQUIRED_ERROR,
        }
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            'required': PASSWORD_REQUIRED_ERROR,
            'blank': PASSWORD_REQUIRED_ERROR,
        }
    )

    class Meta:
        model = User
        fields = ('password', 'password2')

    def validate(self, attrs):
        """
        This function will match both password, if not same then raise Validation error.
        :rtype: dict
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": PASSWORD_MISMATCH})

        return attrs

    def update(self, instance, validated_data):
        """
        This function will update new password of user.
        :rtype: User object
        """
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class ChangePasswordSerializer(PasswordSerializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            'required': PASSWORD_REQUIRED_ERROR,
            'blank': PASSWORD_REQUIRED_ERROR,
        }
    )

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate_old_password(self, value):
        """
        This function will check user's password matches or not. If not, it will raise Serializer error.
        :rtype: dict
        """
        if not self.instance.check_password(value):
            raise serializers.ValidationError(INCORRECT_OLD_PASSWORD)
        return value


class RestorePasswordSerializer(PasswordSerializer):
    pass

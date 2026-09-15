from rest_framework import serializers, status
from django.utils import timezone
from datetime import timedelta

from .models import UserModel, UserProfileModel


class UserProfileSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()

    class Meta:
        model = UserProfileModel
        # fields = '__all__'
        exclude = ['id', 'user']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = UserModel
        exclude = ('password', 'last_login')


class LoginEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=3)



class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ["email","username",'phone',"password","password2"]

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("پسورد باید حداقل 8 کاراکتر باشد")
        if value == "":
            raise serializers.ValidationError("پسورد نمی‌تواند خالی باشد")
        if value.isdigit():
            raise serializers.ValidationError("پسورد نمی‌تواند فقط شامل اعداد باشد")
        if value.isalpha():
            raise serializers.ValidationError('پسورد نمی تواند فقط شامل حروف باشد')
        if value.isupper():
            raise serializers.ValidationError('پسورد نمی تواند فقط شامل حروف بزرگ باشد')
        if value.islower():
            raise serializers.ValidationError('پسورد نمی تواند فقط شامل حروف کوچک باشد')
        return value

    def validate_phone(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("شماره تلفن باید 11 رقم باشد")
        if not value.isdigit():
            raise serializers.ValidationError("شماره تلفن باید فقط شامل اعداد باشد")
        return value

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("نام کاربری باید حداقل 3 کاراکتر باشد")
        if not value.isalpha():
            raise serializers.ValidationError("نام کاربری باید فقط شامل حروف باشد")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "پسوردها یکسان نیستند"}, code=status.HTTP_400_BAD_REQUEST)

        if attrs['username'] == attrs["password"]:
            raise serializers.ValidationError({"username": "نام کاربری نمی‌تواند با پسورد یکسان باشد"}, code=status.HTTP_400_BAD_REQUEST)
        return attrs

    # def create(self, validated_data):
    #     validated_data.pop("password2")
    #
    #     user = User.objects.create_user(
    #         email=validated_data["email"],
    #         username=validated_data["username"],
    #         phone=validated_data["phone"],
    #         password=validated_data["password"]
    #     )
    #
    #     return user


class VerifyEmailRegisterOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField(default=1234)

    def validate_code(self, value):
        if len(str(value)) < 4:
            raise serializers.ValidationError("کد تایید باید 4 رقم باشد")
        if len(str(value)) > 4:
            raise serializers.ValidationError("کد تایید باید 4 رقم باشد")

        return value



class ChangePasswordUserSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"password": "رمزهای جدید یکسان نیستند"})
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("رمز فعلی اشتباه است")
        return value


    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("پسورد باید حداقل 8 کاراکتر باشد")
        if value == "":
            raise serializers.ValidationError("پسورد نمی‌تواند خالی باشد")
        if value.isdigit():
            raise serializers.ValidationError("پسورد نمی‌تواند فقط شامل اعداد باشد")
        if value.isalpha():
            raise serializers.ValidationError('پسورد نمی تواند فقط شامل حروف باشد')
        if value.isupper():
            raise serializers.ValidationError('پسورد نمی تواند فقط شامل حروف بزرگ باشد')
        if value.islower():
            raise serializers.ValidationError('پسورد نمی تواند فقط شامل حروف کوچک باشد')
        return value


    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()

        return user




class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()



class VerifyForgotPasswordResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)


class AcceptResetPasswordForgotSerializer(serializers.Serializer):
    reset_token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError("رمزها یکسان نیستند")
        return attrs



class OTPTimeSerializer(serializers.Serializer):
    time = serializers.SerializerMethodField()

    def get_time(self, obj):

        remaining = (obj.created_at + timedelta(minutes=2)) - timezone.now()
        seconds = max(int(remaining.total_seconds()), 0)
        minutes = seconds // 60
        seconds = seconds % 60

        return f"{minutes:02d}:{seconds:02d}"
import secrets
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    LoginEmailSerializer,
    OTPTimeSerializer,
    VerifyOTPSerializer,
    VerifyEmailRegisterOTPSerializer,
    RegisterSerializer,
    ChangePasswordUserSerializer,
    ForgotPasswordSerializer,
    VerifyForgotPasswordResetOTPSerializer,
    AcceptResetPasswordForgotSerializer

)
from .models import (
    UserModel,
    UserProfileModel,
    UserOTPModel,
    RegisterUserOTPModel,
    ForgotPasswordResetOTPModel,

)

from rest_framework import status
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


class UserLoginEmailView(APIView):
    # throttle_classes = (AnonRateThrottle,)
    serializer_class = LoginEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = UserModel.objects.using("default").filter(email=email, is_active=True).first()
        if not user or not user.check_password(password):
            return Response(
                {'message': 'اطلاعات وارد شده نادرست است.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        code = secrets.choice(range(1000, 9999))

        last_otp = UserOTPModel.objects.using("default").filter(user=user).first()

        if last_otp:
            if not last_otp.expired_otp():
                time_serializer = OTPTimeSerializer(last_otp)
                return Response({
                    'message': 'کد تایید قبلی هنوز منقضی نشده است.',
                    'remaining_time': time_serializer.data['time'],
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        try:
            UserOTPModel.objects.using("default").update_or_create(
                user=user,
                defaults={
                    'created_at': timezone.now(),
                    'otp_code': code
                }
            )

            return Response({
                "message": 'کد ارسال شد',
                "user_email": user.email,
                "code": code
            })

        except Exception as e:
            return Response({'message': 'خطا در ایجاد کد تایید.'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserEmailOTPView(APIView):
    serializer_class = VerifyOTPSerializer

    # throttle_classes = (AnonRateThrottle,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        otp_code = int(serializer.validated_data['code'])

        otp = UserOTPModel.objects.using("default").select_related("user").filter(user__email=email,
                                                                                  otp_code=otp_code).first()

        if not otp:
            return Response({
                'message': 'کد اشتباه است.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if otp.expired_otp():
            otp.delete()
            return Response({
                'message': 'کد منقضی شده است.'
            }, status=status.HTTP_400_BAD_REQUEST)

        otp.delete()
        refresh = RefreshToken.for_user(otp.user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        )


class RegisterUserView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        code = secrets.choice(range(1000, 9999))

        try:

            RegisterUserOTPModel.objects.using("default").update_or_create(
                email=email,
                defaults={
                    'username': username,
                    'phone': phone,
                    'password': password,
                    'code': code,
                })

            return Response({
                'message': 'کد تایید ارسال شد',
                'response': request.data

            }, status=status.HTTP_200_OK)


        except Exception as e:
            return Response({'message': f'{e} خطا در ارسال کد تایید.'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyRegisterUserEmailOTPView(APIView):
    serializer_class = VerifyEmailRegisterOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        code = int(serializer.validated_data['code'])

        otp = RegisterUserOTPModel.objects.using("default").filter(email=email, code=code).first()

        if not otp:
            return Response({
                'message': 'کد اشتباه است.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if otp.expired_otp():
            otp.delete()
            return Response({
                'message': 'کد منقضی شده است.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserModel.objects.db_manager("default").create_user(
                email=email,
                username=otp.username,
                phone=otp.phone,
                password=otp.password
            )

            UserProfileModel.objects.using("default").create(user=user)
            otp.delete()
            return Response({'message': 'ثبت نام با موفقیت انجام شد.'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': f'{e} خطا در ثبت نام.'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordUserView(APIView):
    serializer_class = ChangePasswordUserSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(request.data, status=status.HTTP_200_OK)


class ForgetPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        user = UserModel.objects.using("default").filter(email=email, is_active=True).first()
        if not user:
            return Response({
                'message': 'کاربری با این ایمیل یافت نشد.'
            }, status=status.HTTP_400_BAD_REQUEST)

        last_otp = ForgotPasswordResetOTPModel.objects.using("default").filter(user=user).first()

        if last_otp:
            if not last_otp.expired_otp():
                time_serializer = OTPTimeSerializer(last_otp)
                return Response(
                    {
                        'message': 'کد تایید قبلی هنوز منقضی نشده است.',
                        'remaining_time': time_serializer.data['time'],
                    }, status=status.HTTP_429_TOO_MANY_REQUESTS)

            if last_otp.expired_otp():
                last_otp.delete(using="default")
                return Response({'message': 'کد منقضی شده است.'}, status=status.HTTP_400_BAD_REQUEST)

        code = secrets.choice(range(1000, 9999))

        try:
            ForgotPasswordResetOTPModel.objects.using("default").select_related("user").update_or_create(
                user=user,
                defaults={
                    'code': code,
                    'created_at': timezone.now()
                }
            )

            return Response({
                'message': 'کد تایید ارسال شد',
                'user_id': user.id,
                'code': code
            }, status=status.HTTP_200_OK)

        except Exception as e:

            return Response({
                'message': f'خطا در ارسال کد تایید: {e}'
            }, status=status.HTTP_400_BAD_REQUEST)


class VerifyForgotPasswordResetOTPView(APIView):
    serializer_class = VerifyForgotPasswordResetOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        otp_code = ForgotPasswordResetOTPModel.objects.using("default").select_related("user").filter(user__email=email,
                                                                                                      code=code).first()

        if not otp_code:
            return Response({"message": "کد اشتباه است"}, status=status.HTTP_400_BAD_REQUEST)
        if otp_code.expired_otp():
            otp_code.delete(using="default")
            return Response({"message": "کد منقضی شده است"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_code.reset_token = uuid.uuid4()
            otp_code.save(using="default")

            return Response({
                "message": "کد تایید معتبر است",
                "reset_token": otp_code.reset_token,
                "code": otp_code.code,
            })
        except Exception as e:
            return Response({'message': f'{e} خطا در ایجاد توکن بازنشانی رمز عبور'})


class AcceptForgotPasswordResetOTPView(APIView):
    serializer_class = AcceptResetPasswordForgotSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data['reset_token']
        otp_code = ForgotPasswordResetOTPModel.objects.using("default").filter(reset_token=token).first()

        if not otp_code:
            return Response({"message": 'توکن نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)
        if otp_code.expired_otp():
            otp_code.delete(using="default")
            return Response({"message": "توکن منقضی شده است"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = otp_code.user
            user.set_password(serializer.validated_data['new_password'])
            otp_code.delete(using="default")
            user.save(using="default")
            return Response({'message': 'رمز عبور با موفقیت تغییر یافت'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'{e} خطا در تغییر رمز عبور'}, status=status.HTTP_400_BAD_REQUEST)

from .models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .serializers import LoginSerializer, UserSerializer, ChangePasswordSerializer, UserProfileSerializer
from enrollments.models import Enrollment
from enrollments.serializers import EnrollmentSerializer
from django.core.cache import cache
from django.core.mail import send_mail
import random


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        email = data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = str(random.randint(100000, 999999))

        cache.set(f"pending_user_{email}", data, timeout=300)
        cache.set(f"otp_{email}", otp_code, timeout=300)

        send_mail(
            subject="Your OTP for Email Verification",
            message=f"Your OTP is {otp_code}",
            from_email="from@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent to your email. Please verify."}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        otp_code = request.data.get("otp_code")

        if not email or not otp_code:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        stored_otp = cache.get(f"otp_{email}")
        user_data = cache.get(f"pending_user_{email}")

        if not stored_otp or not user_data:
            return Response({"error": "OTP expired or invalid request."}, status=status.HTTP_400_BAD_REQUEST)

        if stored_otp != otp_code:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            phone=user_data["phone"],
            password=user_data["password"]
        )
        user.is_verified = True
        user.is_active = True
        user.save()

        cache.delete(f"otp_{email}")
        cache.delete(f"pending_user_{email}")

        return Response({"message": "Email verified successfully. Account created!"}, status=status.HTTP_201_CREATED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={"request": request})
        return Response(serializer.data)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(user=request.user)
        enrollments_data = EnrollmentSerializer(enrollments, many=True, context={"request": request}).data

        dashboard_data = {
            "welcome_message": f"Welcome, {request.user.first_name}!",
            "user": {
                "id": request.user.id,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "phone": request.user.phone,
                "role": request.user.role,
                "profile_picture": request.build_absolute_uri(request.user.profile_picture.url) 
                    if request.user.profile_picture else None,
                "bio": request.user.bio,
            },
            "enrollments": enrollments_data,
        }

        return Response(dashboard_data, status=status.HTTP_200_OK)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class RequestPasswordResetOTPView(APIView):
    """
    Sends an OTP to the user's email for password reset.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "No account found with this email."}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = str(random.randint(100000, 999999))
        
        cache.set(f"password_reset_otp_{email}", otp_code, timeout=300)  # ✅ Expiry: 5 minutes

        send_mail(
            subject="Your OTP for Password Reset",
            message=f"Your OTP for password reset is {otp_code}",
            from_email="from@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)


class VerifyPasswordResetOTPView(APIView):
    """
    Verifies the OTP and generates a token for password reset.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp_code = request.data.get("otp_code")

        if not email or not otp_code:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        stored_otp = cache.get(f"password_reset_otp_{email}")

        if not stored_otp:  # ✅ If OTP is expired, return error
            return Response({"error": "OTP expired or invalid request."}, status=status.HTTP_400_BAD_REQUEST)

        if stored_otp != otp_code:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(user)

        cache.set(f"password_reset_token_{email}", token, timeout=300)  # ✅ Expiry: 5 minutes

        return Response({
            "message": "OTP verified. Use the token to reset your password.",
            "email": email,
            "token": token
        }, status=status.HTTP_200_OK)



class SetNewPasswordView(APIView):
    """
    Sets a new password using the token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not email or not token or not new_password:
            return Response({"error": "Invalid request data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email."}, status=status.HTTP_400_BAD_REQUEST)

        stored_token = cache.get(f"password_reset_token_{email}")

        if not stored_token or stored_token != token:  # ✅ If token expired, return error
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        # Reset the password
        user.set_password(new_password)
        user.save()

        # Clear the token from cache
        cache.delete(f"password_reset_token_{email}")

        return Response({"message": "Password updated successfully. You can now login with your new password."}, status=status.HTTP_200_OK)

from .models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserSerializer, ChangePasswordSerializer, UserProfileSerializer
from enrollments.models import Enrollment
from enrollments.serializers import EnrollmentSerializer
from django.core.cache import cache
from django.core.mail import send_mail
import random


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Step 1: Receive user details, generate OTP, and send email.
        """
        data = request.data
        email = data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a 6-digit OTP
        otp_code = str(random.randint(100000, 999999))

        # Temporarily store user details in cache for 5 minutes
        cache.set(f"pending_user_{email}", data, timeout=300)  # 300 seconds (5 minutes)
        cache.set(f"otp_{email}", otp_code, timeout=300)

        # Send OTP via Email
        send_mail(
            subject="Your OTP for Email Verification",
            message=f"Your OTP is {otp_code}",
            from_email="iamnishankhan@gmail.com",  # Replace with actual email
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent to your email. Please verify."}, status=status.HTTP_200_OK)
        

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Step 2: Verify OTP and create the user account.
        """
        email = request.data.get("email")
        otp_code = request.data.get("otp_code")

        if not email or not otp_code:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve stored OTP from cache
        stored_otp = cache.get(f"otp_{email}")
        user_data = cache.get(f"pending_user_{email}")

        if not stored_otp or not user_data:
            return Response({"error": "OTP expired or invalid request."}, status=status.HTTP_400_BAD_REQUEST)

        if stored_otp != otp_code:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # OTP is valid, create the user
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

        # Clear temporary data
        cache.delete(f"otp_{email}")
        cache.delete(f"pending_user_{email}")

        return Response({"message": "Email verified successfully. Account created!"}, status=status.HTTP_201_CREATED)



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={"request": request})  # ✅ Pass request context
        return Response(serializer.data)
    

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch user's enrollments
        enrollments = Enrollment.objects.filter(user=request.user)

        # ✅ Pass `request` context to `EnrollmentSerializer`
        enrollments_data = EnrollmentSerializer(enrollments, many=True, context={"request": request}).data

        # Dashboard response with user data and cleaned enrollments
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
            "enrollments": enrollments_data,  # ✅ Now includes full `thumbnail` URL
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
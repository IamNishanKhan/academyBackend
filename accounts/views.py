from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, ChangePasswordSerializer, UserProfileSerializer
from enrollments.models import Enrollment
from enrollments.serializers import EnrollmentSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


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
        print("Received Login Request Data:", request.data)  # Debugging log

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

        print("Login Failed - Errors:", serializer.errors)  # Debugging log
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
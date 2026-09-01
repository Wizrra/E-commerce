from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import User, ProfilePicture
from .serializers import UserSerializer, UserRegisterationSerializer, UserLoginSerializer, ProfilePictureSerializer
# jwt
import jwt
from django.conf import settings

# from account.utils.emails import send_otp_email_task
from accounts.utils.otp import generate_send_otp, verify_otp
from accounts.utils.handle_cookie import set_session_cookie, set_access_refresh_tokens
from rest_framework import permissions


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # generate and send otp to user email
        generate_send_otp(user)
        response = Response({
            'message': 'User registered successfully. Please check your email for the OTP to verify your account.'}, status=status.HTTP_201_CREATED)
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # generate and send otp to user email
        generate_send_otp(user)
        response = Response({
            'message': 'User registered successfully. Please check your email for the OTP to verify your account.'}, status=status.HTTP_201_CREATED)
        return set_session_cookie(response, user.id)
    

class VerifyOTPView(APIView):
    def post(self, request):
        otp = request.data.get('otp')

        # get jwt token from cookie
        user_id = request.COOKIES.get('session_token')
        if not user_id:
            return Response({'message': 'Session token not found.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            payload = jwt.decode(user_id, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return Response({'error': 'Invalid session token.'}, status=status.HTTP_400_BAD_REQUEST)

        # verify otp
        if verify_otp(user, otp):
            user.is_verified = True
            user.is_active = True
            user.save()
            
            ProfilePicture.objects.create(user=user)  # Create a default profile picture for the user
            return Response({'message': 'OTP verified successfully. Your account is now active.'}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid OTP. Please try again."}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_verified:
            # Resend OTP if user is not verified
            generate_send_otp(user)
            # set a cookie with user id to verify otp later
            response = Response({'message': 'User is not verified. A new OTP has been sent to your email.'}, status=status.HTTP_400_BAD_REQUEST)
            return set_session_cookie(response, user.id)
           
        response = Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        return set_access_refresh_tokens(response, user)


class ProfilePictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        existing = ProfilePicture.objects.filter(user=request.user).first()
        if existing:
          serializer = ProfilePictureSerializer(existing, data=request.data, partial=True)
          if not serializer.is_valid():
              return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
          serializer.save()
        response = Response({'message': 'Profile picture uploaded successfully.'}, status=status.HTTP_201_CREATED)

      # No existing profile picture, create a new one
        serializer = ProfilePictureSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save(user=request.user)
        except Exception as exc:
            # catch DB integrity error and return structured Json
          return Response({"error": "Could not save profile picture", "details": str(exc)}, status=status.HTTP_500_InTERNAL_SERVER_ERROR)
        return Response({"message": "Profile picture uploaded successfully."}, status=status.HTTP_201_CREATED)

    def get(self, request):
        profile_pictures = ProfilePicture.objects.filter(user=request.user).first()
        if not profile_pictures:
            return Response({'message': 'No profile picture found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfilePictureSerializer(profile_pictures)
        return Response(serializer.data, status=status.HTTP_200_OK)
# accounts/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomRegisterSerializer
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework.permissions import AllowAny  # Import AllowAny permission class
from django.http import JsonResponse

from django.contrib.auth import get_user_model 

User = get_user_model()  # Use get_user_model() to get the User model

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Access the verification code from the user object
            verification_code = user.verification_code

            # Send verification code to user via email
            send_mail(
                'Verification Code',
                f'Your verification code is: {verification_code}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )

            return Response({"detail": "Verification code sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        verification_code = request.data.get('verification_code', '')
        email = request.data.get('email', '')

        if not verification_code or not email:
            return JsonResponse({'error': 'Verification code and email are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email, verification_code=verification_code)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)

        # Activate the user account
        user.is_active = True
        user.save()

        return JsonResponse({'detail': 'Account verified and activated successfully.'}, status=status.HTTP_200_OK)
# core/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from .models import UserDetail
from .serializers import UserDetailSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if user already exists
        if UserDetail.objects.filter(email=request.data['email']).exists():
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        return Response({
            'message': 'User registered successfully.',
            'user': {
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = UserDetail.objects.get(email=email)
            if not check_password(password, user.password):
                return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'message': 'Login successful!',
                'user': {
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)
        except UserDetail.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

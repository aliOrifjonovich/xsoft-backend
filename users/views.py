from django.shortcuts import render
import re, json
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from drf_yasg import openapi

import random
import string,secrets
from rest_framework import viewsets

from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from app.utils import notification
from app.models.notification import MessageLog

from app.pagination .paginations import DefaultLimitOffSetPagination

from .serializer import RequestUserSerializer,UserSerializer,UserRoleSerializer,UserCreateSerializer

from .models import User,UserRole

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    pagination_class = DefaultLimitOffSetPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter().order_by("-updated_at")
    serializer_class = UserSerializer
    pagination_class = DefaultLimitOffSetPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateSerializer
        return RequestUserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Generate a secure temporary password and OTP
        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        otp = random.randint(100000, 999999)

        # Save the user with the temporary password and mark as inactive
        user = serializer.save(
            is_active=False,
            password=make_password(temp_password),
        )

        return Response(
            {
                "message": "User created successfully. OTP and temporary password sent to email.",
                "user_id": user.id,
                "password":temp_password
            },
            status=status.HTTP_201_CREATED
        )
            

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'identifier': openapi.Schema(type=openapi.TYPE_STRING, description='User identifier, could be email or phone number'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
        },
        required=['identifier', 'password'],
    )
)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    identifier = request.data.get('identifier')
    password = request.data.get('password')
    
    if not identifier or not password:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        validate_email(identifier)
        is_email = True
    except ValidationError:
        is_email = False
    
    if is_email:
        user = User.objects.filter(email=identifier).first()
    else:
        user = User.objects.filter(phone_number=identifier).first()
    
    if user and user.check_password(password):
        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={
        200: RequestUserSerializer(),
        401: openapi.Response("User not authenticated", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message")
            }
        )),
        404: openapi.Response("No info found", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message")
            }
        )),
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    try:
        print(f"{request.user.pk}")
        user_data = User.objects.get(id=request.user.pk)
        serializer= RequestUserSerializer(user_data)
        data = serializer.data
        return Response(data,status=200)
    except Exception as e:
        return Response({"error": f"{e}"}, status=404)

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the homepage!")

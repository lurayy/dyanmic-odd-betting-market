from django.conf import settings
from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from core.utils.functions import grab_error, is_token_valid
from .serializers.userbase import UserBaseSerializer


def authenticate_user(email, password):
    user = authenticate(email=email, password=password)
    if not user:
        raise Exception("Email or password wrong.")
    tokens = RefreshToken.for_user(user)
    tokens = {"access": str(tokens.access_token), "refresh": str(tokens)}
    cache.set(
        tokens["access"],
        tokens["refresh"],
        settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
    )
    cache.set(
        tokens["refresh"],
        tokens["access"],
        settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
    )
    details = UserBaseSerializer(instance=user).data
    cache.set(
        f'user_{tokens["refresh"]}',
        user,
        settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
    )
    return (tokens, details)


@api_view(["POST"])
@grab_error
def login(request):
    """
    Returns a JWT token.
    {
        'email'- __str__,
        'password'- __str__
    }
    """
    email = str(request.data["email"])
    password = str(request.data["password"])
    token, details = authenticate_user(email, password)
    return Response({"tokens": token, "user_details": details})


@api_view(["GET"])
@grab_error
def whoami(request):
    if request.user.is_authenticated:
        return Response({
            "status": True,
            "data": UserBaseSerializer(instance=request.user).data
        })
    else:
        return Response({
            "status": False,
            "msg": "Anonymous User."
        },
                        status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@permission_classes([AllowAny])
@grab_error
def login_refresh(request):
    data = request.data
    if not is_token_valid(data["refresh"]):
        raise Exception("Passed refresh is blacklisted. Try logging in.")
    auth_token = cache.get(data["refresh"])
    user = cache.get(f'user_{data["refresh"]}')
    x = TokenRefreshSerializer(data=data)
    try:
        x.is_valid(raise_exception=True)
    except Exception as e:
        raise Exception(e.args[0])
    tokens = {
        "access": x.validated_data["access"],
        "refresh": x.validated_data["access"],
    }
    cache.delete(auth_token)
    cache.delete(data["refresh"])
    cache.delete(f'user_{data["refresh"]}')

    cache.set(
        tokens["access"],
        tokens["refresh"],
        settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
    )
    cache.set(
        tokens["refresh"],
        tokens["access"],
        settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
    )
    cache.set(
        f'user_{tokens["refresh"]}',
        user,
        settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
    )
    return Response(tokens, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@grab_error
def logout(request):
    """
    Invalidates current JWT token.


    Call Logout after user logs out and also remember to delete the token from
    local storage.

    """
    refresh_token = cache.get(request.auth)
    cache.delete(refresh_token)
    cache.delete(request.auth)
    cache.delete(f"user_{refresh_token}")
    return Response({"status": True})

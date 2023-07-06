from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers.userbase import UserBaseSerializer, RegisterUserBaseSerializer

from users.models import UserBase
from .auth import authenticate_user


class RegisterUserBaseAPI(GenericAPIView):
    serializer_class = RegisterUserBaseSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token, details = authenticate_user(request.data['email'],
                                               request.data['password'])
            return Response({"tokens": token, "user_details": details})
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class UserBaseAPI(ModelViewSet):
    serializer_class = UserBaseSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["first_name", "last_name", "email"]
    filterset_fields = ["first_name", "last_name", "email"]
    ordering_fields = ["created_at", "id"]
    order = "-id"
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserBase.objects.filter().order_by('-id')
        return UserBase.objects.filter(id=self.request.user.id).order_by('-id')

    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, args, kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, args, kwargs)

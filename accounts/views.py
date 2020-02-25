from django.contrib.auth.models import Group
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username']

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPWSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({'detail':'密码重置成功'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePWSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = self.serializer_class(
                data=request.data,
                context={'user':request.user})

        if serializer.is_valid():
            serializer.save()

            return Response({'detail':'密码修改成功'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

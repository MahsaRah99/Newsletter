from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class UserRegisterView(APIView):
    """Handles user registration."""

    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):
    """This view set provides endpoints for listing, retrieving, updating, and
    deactivating user accounts."""

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)

    def list(self, request):
        """Retrieves a list of active users."""
        srz_data = self.serializer_class(instance=self.queryset, many=True)
        return Response(srz_data.data)

    def retrieve(self, request, pk=None):
        """Retrieves details of the specified user."""
        user = get_object_or_404(self.queryset, pk=pk)
        srz_data = self.serializer_class(instance=user)
        return Response(srz_data.data)

    def partial_update(self, request, pk=None):
        """Edits the specified user with the provided data."""
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({"permission denied": "you are not the owner"})
        srz_data = UserSerializer(instance=user, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data)
        return Response(data=srz_data.errors)

    def destroy(self, request, pk=None):
        """Deactivates a user's account"""
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({"permission denied": "you are not the owner"})
        user.is_active = False
        user.save()
        return Response({"message": "user deactivated"})

from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    # for special return after serializer.save():
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "User created.",
                "username": request.data.get("username"),
                "email": request.data.get("email"),
                "first_name": request.data.get("first_name"),
                "last_name": request.data.get("last_name"),
            }
        )
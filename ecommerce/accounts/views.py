from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate
from accounts.serializer import UserSerializer
# Create your views here.

class RegisterView(CreateAPIView):
    serializer_class = UserSerializer

class LoginView(ViewSet):
    def create(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username,password=password)
        if user:
            token,created = Token.objects.get_or_create(user=user)
            return Response(data={
                "msg":"User is login succefully!!!!",
                "username":user.username,
                "token_key":token.key,
                "created":created,
                "user_id":user.id,
            },status=status.HTTP_200_OK)
        return Response(data={"msg":"Invalid user"},status=status.HTTP_400_BAD_REQUEST)


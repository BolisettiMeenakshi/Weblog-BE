from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import User
from .userSerializer import UserSerializer
from rest_framework.response import Response
import jwt
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework import generics

SECRET_KEY = "secret-key"

@api_view(["POST"])
def login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"msg": "Username and password are required."}, status=400)

        user = User.objects.get(username=username)
        user_data = UserSerializer(user).data
        if user_data["password"] != password:
            return Response({
                "msg": "Login Failed - Incorrect credentials",
                "login": 0
            }, status=401)

        payload = {
            "userId": user_data["id"],
            "username": user_data["username"],
            "email": user_data["email"],
            "exp": datetime.utcnow() + timedelta(hours=2),
            "iat": datetime.utcnow(),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return Response({
            "msg": "Login Success",
            "token": token,
            "login": 1,
            "code": "100"
        })

    except User.DoesNotExist:
        return Response({"msg": "User does not exist."}, status=404)

    except Exception as err:
        return Response({
            "msg": "An error occurred.",
            "error": str(err)
        }, status=500)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "msg": "Registration successful.",
            "user": serializer.data
        }, status=201)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def verify(request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"msg": "Authorization token missing or invalid."}, status=401)

        token = auth_header.split(" ")[1]
        user_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        return Response({
            "msg": "User token is verified.",
            "userData": user_data
        })

    except jwt.ExpiredSignatureError:
        return Response({"msg": "Token has expired."}, status=401)

    except jwt.InvalidTokenError:
        return Response({"msg": "Invalid token."}, status=401)

    except Exception as err:
        return Response({"msg": "An error occurred.", "error": str(err)}, status=500)

@api_view(["POST"])
def logout(request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"msg": "Authorization token missing or invalid."}, status=401)

        token = auth_header.split(" ")[1]

        return Response({
            "msg": "Logout successful. Please remove the token from client storage."
        }, status=200)

    except Exception as err:
        return Response({
            "msg": "An error occurred during logout.",
            "error": str(err)
        }, status=500)
class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

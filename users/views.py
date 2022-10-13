from rest_framework.views import APIView, Request, Response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser

from .permissions import IsAdmOrOwner

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from users.models import User

from .serializers import LoginSerializer, UserSerializer


class UserRegisterView(APIView):
    def post(self, req: Request) -> Response:
        serializer = UserSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, req: Request) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)


class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmOrOwner]

    def get(self, req: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(req, user)

        serializer = UserSerializer(user)

        return Response(serializer.data)


class UserAuthToken(ObtainAuthToken):
    def post(self, req: Request) -> Response:
        serializer = LoginSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})

        return Response(
            {"detail": "invalid username or password"},
            status.HTTP_400_BAD_REQUEST,
        )

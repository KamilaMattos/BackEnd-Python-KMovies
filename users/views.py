from rest_framework.views import APIView, Request, Response, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, UserSerializer
from django.contrib.auth import authenticate


class UserRegisterView(APIView):
    def post(self, req: Request) -> Response:
        serializer = UserSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


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

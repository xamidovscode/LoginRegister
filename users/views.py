from rest_framework import generics
from rest_framework.response import Response
from . import models
from . import serializers
from .permissions import IsAuthenticated, IsStudent
from rest_framework.views import APIView


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    queryset = models.CustomUser.objects.all()


class CodeVerifyAPIView(generics.CreateAPIView):
    serializer_class = serializers.CodeVerificationSerializer
    queryset = models.CustomUser.objects.all()


class LoginAPIView(generics.CreateAPIView):
    serializer_class = serializers.LoginSerializer
    queryset = models.CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        tokens = user.tokens()
        return Response(
            data={
                "data": tokens
            }, status=200
        )


class ResendCodeAPIView(generics.CreateAPIView):
    serializer_class = serializers.ResendCodeSerializer
    queryset = models.CustomUser.objects.all()


class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.ProfileSerializer
    queryset = models.CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class APITEST(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        return Response("success")



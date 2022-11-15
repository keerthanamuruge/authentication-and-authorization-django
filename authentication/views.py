from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from authentication.serializers import RegisterSerializer, LoginSerializer


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data.get('is_tl'):
            serializer.create_tl()
        serializer.save()
        response = {
            "message": "User created successfully"
            }
        return Response(response, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=201)


class Timechamp(GenericAPIView):
    def get(self, request):
        return Response({"ok":"done"})


class TLView(GenericAPIView):
    pass
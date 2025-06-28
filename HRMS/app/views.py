from rest_framework.views import APIView
from .Serilazers import UserSerializer, CustomLoginSerializer
from rest_framework import status
from rest_framework.response import Response


# Create your views here.


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('user created successfully')
        else:
            invalid_data = serializer.errors
            return Response(invalid_data)

class CustomLoginView(APIView):
    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
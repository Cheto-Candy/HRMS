from rest_framework.views import APIView
from .Serilazers import UserSerializer
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
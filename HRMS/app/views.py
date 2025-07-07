from rest_framework.views import APIView
from .Serilazers import  LeaveApplySerializer, UserProfileSerializer, RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import User, Leave
from rest_framework import permissions
from .permission import IsEmployee,IsAdminOrHR

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ApplyLeaveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LeaveApplySerializer(data=request.data)
        if serializer.is_valid():
            # Save with logged-in user
            serializer.save(user=request.user)
            return Response({"msg": "Leave applied successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyLeavesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        leaves = Leave.objects.filter(user=request.user).order_by('-applied_at')
        serializer = LeaveApplySerializer(leaves, many=True)
        return Response(serializer.data)
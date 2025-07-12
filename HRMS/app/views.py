from rest_framework.views import APIView
from .Serilazers import  LeaveApplySerializer,UserProfileUpdateSerializer, UserProfileSerializer, RegisterSerializer, LoginSerializer, AttendanceSerializer,DepartmentSerializer
from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response
from .models import Leave, UserProfile,Attendance,Department
from rest_framework import permissions
from .permission import IsEmployee,IsAdminOrHR
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

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

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsAdminOrHR]

    def patch(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

        serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Profile updated successfully"})
        return Response(serializer.errors, status=400)


class MarkAttendanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        today = timezone.now().date()
        already_marked = Attendance.objects.filter(user=request.user, date=today).exists()

        if already_marked:
            return Response({"detail": "Attendance already marked for today."}, status=400)

        attendance = Attendance.objects.create(user=request.user)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

class MyAttendanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        attendance = Attendance.objects.filter(user=user).order_by('-date')
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)

class AllAttendanceView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrHR]

    def get(self, request):
        attendance = Attendance.objects.all().order_by('-date')
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)


class DepartmentView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrHR]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
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
    
class ManageLeaveView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrHR]

    def get(self, request):
        leaves = Leave.objects.all().order_by('-applied_at')
        serializer = LeaveApplySerializer(leaves, many=True)
        return Response(serializer.data)

    def patch(self, request):
        leave_id = request.data.get("id")
        new_status = request.data.get("status")

        if not leave_id:
            return Response({"error": "Leave ID is required"}, status=400)
        if new_status not in ["Approved", "Rejected"]:
            return Response({"error": "Invalid status"}, status=400)

        try:
            leave = Leave.objects.get(id=leave_id)
        except Leave.DoesNotExist:
            return Response({"error": "Leave not found"}, status=404)

        leave.status = new_status
        leave.save()

        return Response({
            "msg": f"Leave (ID: {leave.id}) updated to {leave.status}"
        }, status=200)
    
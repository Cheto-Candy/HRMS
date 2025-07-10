"""
URL configuration for HRMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from app.views import RegisterView, MyLeavesView, ApplyLeaveView,LoginView,ManageLeaveView,LogoutView,ProfileView,UpdateProfileView,MarkAttendanceView,MyAttendanceView,AllAttendanceView,DepartmentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    # path('', CustomLoginView.as_view(), name='login'),
    path('my_leaves/', MyLeavesView.as_view(), name='my_leaves'),
    path('apply_leave/', ApplyLeaveView.as_view(), name='apply_leave'),
    path('all_leaves/', ManageLeaveView.as_view(), name='all_leaves'),
    path('my-leaves/', MyLeavesView.as_view(), name='my-leaves'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('attendance/mark/', MarkAttendanceView.as_view(), name='mark-attendance'),
    path('attendance/my/', MyAttendanceView.as_view(), name='my-attendance'),
    path('attendance/all/', AllAttendanceView.as_view(), name='all-attendance'),
    path('departments/', DepartmentView.as_view(), name='create-department'),


]

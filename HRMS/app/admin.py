from django.contrib import admin
from .models import Leave, UserProfile, Attendance

# Register your models here.
# admin.site.register(User)

admin.site.register(Leave)
admin.site.register(UserProfile)
admin.site.register(Attendance)
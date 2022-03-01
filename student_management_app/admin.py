from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from student_management_app.models import CustomUser

# Register your models here.

class UserModul(UserAdmin):
    pass

admin.site.register(CustomUser, UserModul)


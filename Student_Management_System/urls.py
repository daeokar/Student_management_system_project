"""Student_Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from student_management_app import *
from student_management_app import views
from student_management_app.HodViews import *
from student_management_app.staff_view import *
from student_management_app.student_view import *

urlpatterns = [

    # path('admin/', admin.site.urls),
    path('demo/', views.Demo_page, name='demo'),
    path('login/', views.show_login_page, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('get_user_details/', views.GetUserDetails, name='get_user_details'),
    path('Logout', views.logout_user, name='Logout'),
    path('admin_home/', AdminHome, name='admin_home'),
    path('add_staff/', add_staff, name='add_staff'),
    path('add_staff_save', add_staff_save, name='add_staff_save'),
    path('add_course/', add_course, name='add_course'),
    path('add_courses_save', add_courses_save, name='add_courses_save'),
    path('add_student/', add_student, name='add_student'),
    path('add_student_save', add_student_save, name='add_student_save'),
    path('add_subject', add_subject, name='add_subject'),
    path('add_subject_save', add_subject_save, name='add_subject_save'),
    path('manage_staff', manage_staff, name='manage_staff'),
    path('manage_student', manage_student, name='manage_student'),
    path('manage_course', manage_course, name='manage_course'),
    path('manage_subject', manage_subject, name='manage_subject'),
    path('edit_staff/<str:staff_id>', edit_staff, name='login'),
    path('edit_staff_save', edit_staff_save, name='edit_staff_save'),
    path('edit_student/<str:student_id>', edit_student, name='edit_student'),
    path('edit_student_save', edit_student_save, name='edit_student_save'),
    path('edit_subject/<str:subject_id>', edit_subject, name='edit_subject'),
    path('edit_subject_save', edit_subject_save, name='edit_subject_save'),
    path('edit_course/<str:course_id>', edit_course, name='edit_course'),
    path('edit_course_save', edit_course_save, name='edit_course_save'),
    path('manage_sessions', manage_sessions, name='manage_sessions'),
    path('add_session_save', add_session_save, name='add_session_save'),


  #------Staff Url Path
    path('staff_home', staff_home, name='staff_home'),
    path('staff_take_attendance', staff_take_attendance, name='staff_take_attendance'),
    path('get_students', get_students, name='get_students'),
    path('save_attendance_date', save_attendance_date, name='save_attendance_date'),


  #-----student url path
    path('student_home', student_home, name='student_home'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)





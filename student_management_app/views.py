# from urllib import request
# from pyexpat.errors import messages
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_management_app.EmailBackEnd import EmailBackEnd
# from student_management_app.staff_view import staff_home
# from student_management_app.student_view import student_home

# Create your views here.

def Demo_page(request):
    return render(request, "demo.html")

def show_login_page(request):
    return render(request, "login_page.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h1> Method Not Allowed </h1>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect("/admin_home")
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponse(reverse("student_home"))
            # return HttpResponse("Email :"+request.POST.get("email") +"Password :"+request.POST.get("password")  )
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("login/")

def GetUserDetails(request):
    if request.method != None:
        return HttpResponse("User : "+request.user.email +"usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("login/")

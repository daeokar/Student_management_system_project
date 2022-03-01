
# import email

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_management_app.forms import *
from student_management_app.models import (Courses, CustomUser, Staffs,
                                           Students, Subjects)


def AdminHome(request):
    return render(request, "hod_template/home_content.html/")


def add_staff(request):
    return render(request, "hod_template/add_staff_template.html/")

def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


def add_course(request):
    return render(request, "hod_template/add_course_template.html/")


def add_courses_save(request):
    if request.method != "POST":
        return HttpResponse("<h1>Method not ALlowed</h1>")
    else:
        course = request.POST.get("Course")
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))

        except:
            messages.error(request, "Failed to Add Course")
            return HttpResponseRedirect(reverse("add_course"))

def add_student(request):
    form = AddStudentForm()
    return render(request, "hod_template/add_student_template.html/", {"form" : form})

def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h1>Method Not Allowed</h1>")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]
            # print(request.FILES['profile_pic'])
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email, user_type=3)
                user.students.address = address
                course_object = Courses.objects.get(id=course_id)
                user.students.course_id = course_object
                session_year = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year
                user.students.gender = sex
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request, "Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form = AddStudentForm(request.POST)
            return render(request, "hod_template/add_student_template.html/", {"form" : form})



def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/add_subject_template.html",{"staffs" : staffs, "courses" : courses})



def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h1>Method Not Allowed</h1>")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)

        try:
            subject=Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))

def manage_staff(request):
    staff = Staffs.objects.all()
    return render(request, "hod_template/manage_staff_template.html", {"staffs" : staff})


def manage_student(request):
    students = Students.objects.all()
    return render(request, "hod_template/manage_student_template.html", {"students" : students})


def manage_course(request):
    courses = Courses.objects.all()
    return render(request, "hod_template/manage_course_temoplate.html", {"courses" : courses})

def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, "hod_template/manage_subject_template.html", {"subjects" : subjects})



def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request, "hod_template/edit_staff_template.html", {"staff" : staff})


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h1>Method Not Allowed</h1>")

    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id" : staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id" : staff_id}))
    

def edit_student(request, student_id):
    request.session["student_id"] = student_id
    # courses = Courses.objects.all()
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields["email"].initial = student.admin.email
    form.fields["first_name"].initial = student.admin.first_name
    form.fields["last_name"].initial = student.admin.last_name
    form.fields["username"].initial = student.admin.username
    form.fields["address"].initial = student.address
    form.fields["course"].initial = student.course_id.id
    form.fields["sex"].initial = student.gender
    form.fields["session_year_id"].initial = student.session_year_id

    return render(request, "hod_template/edit_student_template.html" , {"form" : form, "student" : student, "id" : student_id, "username" : student.admin.username})




def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h1>Method Not Allowed</h1>")

    else:
        studend_id = request.session.get("student_id")
        if studend_id == None:
            return HttpResponseRedirect(reverse("manage_student"))

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course_id"]
            sex = form.cleaned_data["sex"]

            if request.FILES["profile_pic"]:
                profile_pic = request.FILES["profile_pic"]
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)

            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=studend_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                student = Students.objects.get(admin=studend_id)
                student.address = address
                session_year = SessionYearModel.objects.get(id=session_year_id)
                student.session_year_id = session_year
                student.gender = sex
                
                course = Courses.objects.get(id=course_id)
                student.course_id = course
                if profile_pic_url != None:
                    student.profile_pic = profile_pic_url
                student.profile_pic = profile_pic_url
                student.save()
                del request.session["student_id"]
                messages.success(request,"Successfully Edited Staff")
                return HttpResponseRedirect(reverse("edit_student", kwargs = {"student_id" : studend_id}))
            except:
                messages.error(request,"Failed to Edit Staff")
                return HttpResponseRedirect(reverse("edit_student", kwargs = {"student_id" : studend_id}))
        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=studend_id)
            return render(request, "hod_template/edit_student_template.html", {"form" : form, "id" :studend_id, "username" : student.admin.username})



def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/edit_subject_template.html", {"subject" : subject, "courses" : courses, "staffs" : staffs, "id" : subject_id})


def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            subject.save()
            messages.success(request,"Successfully Edited subject")
            return HttpResponseRedirect(reverse("edit_subject", kwargs = {"subject_id" : subject_id}))
        except:
            messages.error(request,"Failed to Edit subject")
            return HttpResponseRedirect(reverse("edit_subject", kwargs = {"subject_id" : subject_id}))


def edit_course(request,course_id):
    courses = Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course" : courses, "id" : course_id})


def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request,"Successfully Edited course")
            return HttpResponseRedirect(reverse("edit_course", kwargs = {"course_id" : course_id}))
        except:
            messages.error(request,"Failed to Edit course")
            return HttpResponseRedirect(reverse("edit_course", kwargs = {"course_id" : course_id}))



def manage_sessions(request):
    return render(request,"hod_template/manage_sessions_template.html")

def add_session_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("manage_sessions")
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_End")

        try:
            session_year = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            session_year.save()
            messages.success(request,"Successfully Add Session")
            return HttpResponseRedirect(reverse("manage_sessions"))
        except:
            messages.error(request,"Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_sessions"))








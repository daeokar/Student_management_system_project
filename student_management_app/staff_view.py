import json
from django.http import JsonResponse
from django.shortcuts import render

from student_management_app.models import SessionYearModel, Students, Subjects
from django.views.decorators.csrf import csrf_exempt

def staff_home(request):
    return render(request,"staff_template/staff_home_content.html")


def staff_take_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    return render(request, "staff_template/staff_take_attendance.html", {"subjects" : subjects, "session_years" : session_years})

@csrf_exempt 
def get_students(request):
    subject_id = request.POST.get("subject_id")
    session_year = request.POST.get("session_year")

    subject = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.objects.get(id=session_year)
    students = Students.objects.filter(course_id=subject.course_id, session_year_id=session_model)
    list_data = []

    for student in students:
        data_small = {"id" : student.admin.id, "name" : student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
    

@csrf_exempt
def save_attendance_date(request):
    student_id = request.POST.get("student_id")
    subject_id = request.POST.get("subject_id")
    attendance_data = request.POST.get("attendance_data")
    session_year_id = request.POST.get("session_year_id")
    
    print(student_id)
    subject_model = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.objects.get(id=session_year_id)
    json_student = json.loads(student_id)
    # print(data[0]["id"])
    try:
        attendance = Attendance(subject_id=subject_model, attendance_data=attendance_data, session_year_id=session_model)
        attendance.save()

        for stud in json_student:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")



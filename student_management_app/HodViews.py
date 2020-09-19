import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# from student_management_app.forms import EditStudentForm, AddStudentForm
from student_management_app.models import CustomUser, Courses, Subjects, Staffs, Students, SessionYearModel, \
    FeedbackStudents, FeedbackStaff, LeaveReportStudents, LeaveReportStaff, Attendance, AttendanceReport


def admin_home(request):
    student_count=Students.objects.all().count()
    staff_count = Staffs.objects.all().count()
    course_count = Courses.objects.all().count()
    subject_count = Subjects.objects.all().count()

    course_all=Courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]
    for course in course_all:
        subjects=Subjects.objects.filter(course_id=course.id).count()
        students=Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all=Subjects.objects.all()
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
        course=Courses.objects.get(id=subject.course_id.id)
        student_count2=Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count2)

    staffs=Staffs.objects.all()
    attendance_present_list_staff=[]
    attendance_absent_list_staff=[]
    staff_name_list=[]
    for staff in staffs:
        subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
        attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    students_all=Students.objects.all()
    attendance_present_list_student=[]
    attendance_absent_list_student=[]
    student_name_list=[]
    for student in students_all:
        attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
        absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
        leaves=LeaveReportStudents.objects.filter(student_id=student.id,leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves+absent)
        student_name_list.append(student.admin.username)


    return render(request,"hod_template/home_content.html",{"student_count":student_count,"staff_count":staff_count,"course_count":course_count,"subject_count":subject_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"attendance_present_list_staff":attendance_present_list_staff,"attendance_absent_list_staff":attendance_absent_list_staff,"staff_name_list":staff_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student,"student_name_list":student_name_list})

def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Staff Added Successfully")
            return HttpResponseRedirect("/add_staff")
        except:
            messages.error(request, "Failed To Add Staff")
            return HttpResponseRedirect("/add_staff")

def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request, "hod_template/manage_staff_template.html",{"staffs":staffs})

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request, "hod_template/edit_staff_template.html",{"staff":staff})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        staff_id=request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")
        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request, "Staff Details Updated Successfully")
            return HttpResponseRedirect("/edit_staff/"+staff_id)
        except:
            messages.error(request, "Failed To Update Staff Details")
            return HttpResponseRedirect("/edit_staff/"+staff_id)


def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request, "Course Added Successfully")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request, "Failed To Add Course")
            return HttpResponseRedirect("/add_course")

def manage_course(request):
    courses=Courses.objects.all()
    return render(request, "hod_template/manage_course_template.html",{"courses":courses})

def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request, "hod_template/edit_course_template.html",{"course":course})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course_name")
        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=course_name
            course.save()
            messages.success(request, "Course Details Updated Successfully")
            return HttpResponseRedirect("/edit_course/"+course_id)
        except:
            messages.error(request, "Failed To Update Course Details")
            return HttpResponseRedirect("/edit_course/"+course_id)

def add_student(request):
    courses=Courses.objects.all()
    sessions=SessionYearModel.objects.all()
    return render (request,"hod_template/add_student_template.html",{"courses":courses,"sessions":sessions})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        course_id=request.POST.get("course")
        session_year_id=request.POST.get("session_year")
        sex=request.POST.get("sex")

        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        try:
            user=CustomUser.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name,user_type=3)
            user.students.address=address
            course=Courses.objects.get(id=course_id)
            user.students.course_id=course
            session=SessionYearModel.objects.get(id=session_year_id)
            user.students.session_year_id=session
            user.students.gender=sex
            user.students.profile_pic=profile_pic_url
            user.save()
            messages.success(request,"Student Added Successfully")
            return HttpResponseRedirect("/add_student")
        except:
            messages.error(request, "Failed To Add Student")
            return HttpResponseRedirect("/add_student")

def manage_student(request):
    students=Students.objects.all()
    return render(request, "hod_template/manage_student_template.html",{"students":students})

def edit_student(request,student_id):
    student=Students.objects.get(admin=student_id)
    courses=Courses.objects.all()
    sessions=SessionYearModel.objects.all()
    return render(request,"hod_template/edit_student_template.html",{"student":student,"courses":courses,"sessions":sessions})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        student_id=request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        course_id = request.POST.get("course")
        session_year_id = request.POST.get("session_year")
        sex = request.POST.get("sex")

        if request.FILES['profile_pic']:
            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
        else:
            profile_pic_url=None

        try:
            user=CustomUser.objects.get(id=student_id)
            user.first_name=first_name
            user.last_name=last_name
            user.username=username
            user.email=email
            user.save()
            student=Students.objects.get(admin=student_id)
            student.address = address
            course=Courses.objects.get(id=course_id)
            student.course_id=course
            session_year=SessionYearModel.objects.get(id=session_year_id)
            student.session_year_id=session_year
            student.gender=sex
            if profile_pic_url!=None:
                student.profile_pic=profile_pic_url
            student.save()
            messages.success(request,"Student Details Updated Successfully")
            return HttpResponseRedirect("/edit_student/"+student_id)
        except:
            messages.error(request, "Failed To Update Student Details")
            return HttpResponseRedirect("/edit_student/"+student_id)


def add_subject(request):
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html",{"courses":courses,"staffs":staffs})

def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject=Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully")
            return HttpResponseRedirect("/add_subject")
        except:
            messages.error(request, "Failed To Add Subject")
            return HttpResponseRedirect("/add_subject")

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request, "hod_template/manage_subject_template.html",{"subjects":subjects})

def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/edit_subject_template.html",{"subject":subject, "courses":courses, "staffs":staffs})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        course_id=request.POST.get("course")

        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            subject.save()
            messages.success(request,"Subject Details Updated Successfully")
            return HttpResponseRedirect("/edit_subject/"+subject_id)
        except:
            messages.error(request,"Failed To Update Subject Details")
            return HttpResponseRedirect("/edit_subject/"+subject_id)

def add_session(request):
    return render(request, "hod_template/add_session_template.html")

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
             sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
             sessionyear.save()
             messages.success(request,"Successfully Added Session")
             return HttpResponseRedirect(reverse("add_session"))
        except:
            messages.error(request,"Failed To Add Session")
            return HttpResponseRedirect(reverse("add_session"))


def manage_session(request):
    sessions = SessionYearModel.objects.all()
    return render(request, "hod_template/manage_session_template.html", {"sessions": sessions})

def edit_session(request,subject_id):
    pass

def edit_session_save(request):
    pass

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def staff_feedback_message(request):
    feedbacks=FeedbackStaff.objects.all()
    return render(request,"hod_template/staff_feedback_template.html",{"feedbacks":feedbacks})

@csrf_exempt
def staff_feedback_reply(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedbackStaff.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def student_feedback_message(request):
    feedbacks=FeedbackStudents.objects.all()
    return render(request, "hod_template/student_feedback_template.html",{"feedbacks":feedbacks})

@csrf_exempt
def student_feedback_reply(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedbackStudents.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_leave_view(request):
    leave_data=LeaveReportStaff.objects.all()
    return render(request,"hod_template/staff_leave_view.html", {"leave_data":leave_data})

def staff_leave_approve(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_leave_disapprove(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def student_leave_view(request):
    leave_data=LeaveReportStudents.objects.all()
    return render(request, "hod_template/student_leave_view.html", {"leave_data":leave_data})

def student_leave_approve(request,leave_id):
    leave=LeaveReportStudents.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def student_leave_disapprove(request,leave_id):
    leave=LeaveReportStudents.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_year_id = SessionYearModel.objects.all()
    return render(request, "hod_template/admin_view_attendance.html",{"subjects": subjects, "session_year_id": session_year_id})

@csrf_exempt
def admin_get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.objects.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_date=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_date:
        data_small = {"id": student.student_id.admin.id, "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request,"Successfully Updated Profile Details")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request,"Failed To Update Profile Details")
            return HttpResponseRedirect(reverse("admin_profile"))



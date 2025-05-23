from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django_filters.views import FilterView
from django.db.models import F, Q
from django.db.models import Max
from django.db.models import Value, F, CharField
from django.db.models import OuterRef, Subquery
from datetime import datetime
from django.db import IntegrityError
from accounts.decorators import lecturer_required, student_required, parent_required
from datetime import date
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


# from accounts.models import Student
from core.models import Semester
from course.filters import CourseAllocationFilter, ProgramFilter, GradelevelsFilter
from course.forms import (
    CourseAddForm,
    CourseAllocationForm,
    EditCourseAllocationForm,
    ProgramForm,
    UploadFormFile,
    UploadFormVideo,
)
from course.models import (
    # Course,
    CourseAllocation,
    Program,
    Upload,
    UploadVideo,
)

from course.importmodels import (
    Subject as Course,
    Gradelevels,
    Studentregister,
    Studentenrollsubject,
    Teacher,
    Attendance,
    Student,
    Parent,
    Parentstudent,
    Scharges,
    Spayment,
    Grade,
    Benefits
)
from result.models import TakenCourse


# ########################################################
# Program Views
# ########################################################


@method_decorator([login_required, lecturer_required], name="dispatch")
class ProgramFilterView(FilterView):
    filterset_class = GradelevelsFilter    
    template_name = "course/program_list.html"
    
    # if not self.request.user.is_superuser:
    #     filterset_class = GradelevelsFilter   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Programs"
        return context


@login_required
@lecturer_required
def program_add(request):
    if request.method == "POST":
        form = ProgramForm(request.POST)
        if form.is_valid():
            program = form.save()
            messages.success(request, f"{program.title} program has been created.")
            return redirect("programs")
        messages.error(request, "Correct the error(s) below.")
    else:
        form = ProgramForm()
    return render(
        request, "course/program_add.html", {"title": "Add Program", "form": form}
    )


@login_required
def program_detail(request, pk):
    program = get_object_or_404(Gradelevels, ref=pk)    
    courses = Course.objects.filter(grade_level=pk)
    print(pk)
    # credits = {courses.aggregate(total_credits=Sum("credit"))}
    credits = {}
    paginator = Paginator(courses, 10)
    page = request.GET.get("page")
    courses = paginator.get_page(page)
    return render(
        request,
        "course/program_single.html",
        {
            "title": program.grade_level,
            "program": program,
            "courses": courses,
            "credits": credits,
        },
    )






@login_required
def view_attendance(request, course_id):

    
# Get all enrolled sr_id from Studentenrollsubject
    enrolled_ids = Studentenrollsubject.objects.filter(subject=course_id).values_list('sr_id', flat=True)

    # Get all students register entries
    students_register = Studentregister.objects.filter(sr_id__in=enrolled_ids)
    
    # Get all students from Student table
    students = Student.objects.filter(ref__in=students_register.values_list('stud_id', flat=True))
    
    course = get_object_or_404(Course, ref=course_id)    
    
    
    print(course_id)
    # # Example: Fetch related attendance records here
    # attendance_records = Attendance.objects.filter(cl=course_id)
    # print(attendance_records)
    return render(
        request,
        'course/view_attendance.html',   # You will create this HTML page
        {
            'title': f"Attendance for {course.sub_name}",
            'course': course,
            'students': students,
            
        }
    )

@login_required
def save_attendance(request, course_id):
    if request.method == "POST":
        attendance_date = request.POST.get('attendance_date')
        
        if not attendance_date:
            messages.error(request, "Attendance date is required!")
            return redirect('program_detail', pk=course_id)
        
        course = get_object_or_404(Course, ref=course_id)
        print(course_id)
        # Fetch enrolled students
        enrolled_ids = Studentenrollsubject.objects.filter(subject_id=course_id).values_list('sr_id', flat=True)
        students_register = Studentregister.objects.filter(sr_id__in=enrolled_ids)
        students = Student.objects.filter(ref__in=students_register.values_list('stud_id', flat=True))

        # Loop through students and save attendance
        for student in students:
            status = request.POST.get(f"status_{student.ref}")
            if status:
                Attendance.objects.create(
                    date=attendance_date,
                    cl=course_id,
                    present_status=status,
                    stud=student.ref,   # or another field you use for roll number
                    subject_code=course.ref  # or sub_name if you prefer
                )

        messages.success(request, "Attendance saved successfully!")
        return redirect('view_attendance' , course_id=course_id)

    return redirect('view_attendance', course_id=course_id)

@login_required
def attendance_pdf(request, course_id):
    date_str = request.GET.get("date")
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        return HttpResponse("Invalid date format", status=400)

    # Get attendance records
    attendance_records = Attendance.objects.filter(subject_code=course_id, date=date_obj)

    # Collect student IDs from Attendance
    student_ids = [record.stud for record in attendance_records if record.stud]

    # Get Student records matching those IDs
    students = Student.objects.filter(ref__in=student_ids)

    # Map: studentid -> Student object
    student_map = {s.ref: s for s in students}

    seen = set()
    data = []

    for record in attendance_records:
        try:
            student_ref = int(record.stud) if record.stud else None
        except ValueError:
            continue

        if student_ref in seen:
            continue  # Skip if already processed

        student = student_map.get(student_ref)
        if student:
            data.append({
                'student': student,
                'attendance': record,
            })
            seen.add(student_ref)


    # print(student_map)
    # Render to PDF
    template = get_template("course/attendance_pdf.html")  # replace with your actual template
    html = template.render({"data": data, "date": date_obj})

    from xhtml2pdf import pisa
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error rendering PDF", status=500)
    return response








@login_required
@lecturer_required
def program_edit(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == "POST":
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            program = form.save()
            messages.success(request, f"{program.title} program has been updated.")
            return redirect("programs")
        messages.error(request, "Correct the error(s) below.")
    else:
        form = ProgramForm(instance=program)
    return render(
        request, "course/program_add.html", {"title": "Edit Program", "form": form}
    )


@login_required
@lecturer_required
def program_delete(request, pk):
    program = get_object_or_404(Program, pk=pk)
    title = program.title
    program.delete()
    messages.success(request, f"Program {title} has been deleted.")
    return redirect("programs")


# ########################################################
# Course Views
# ########################################################


@login_required
def course_single(request, ref):
    course = get_object_or_404(Course, ref=ref)
    files = Upload.objects.filter(course_id=ref)
   
    videos = UploadVideo.objects.filter(course_id=ref)
    lecturers = Teacher.objects.get(ref=course.teacher_id)
    
    return render(
        request,
        "course/course_single.html",
        {
            "title": course.sub_name,
            "course": course,
            "files": files,
            "videos": videos,
            "lecturers": lecturers,
            "media_url": settings.MEDIA_URL,
        },
    )
    
    


@login_required
@lecturer_required
def course_add(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == "POST":
        form = CourseAddForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(
                request, f"{course.title} ({course.code}) has been created."
            )
            return redirect("program_detail", pk=program.pk)
        messages.error(request, "Correct the error(s) below.")
    else:
        form = CourseAddForm(initial={"program": program})
    return render(
        request,
        "course/course_add.html",
        {"title": "Add Course", "form": form, "program": program},
    )


@login_required
@lecturer_required
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == "POST":
        form = CourseAddForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            messages.success(
                request, f"{course.title} ({course.code}) has been updated."
            )
            return redirect("program_detail", pk=course.program.pk)
        messages.error(request, "Correct the error(s) below.")
    else:
        form = CourseAddForm(instance=course)
    return render(
        request, "course/course_add.html", {"title": "Edit Course", "form": form}
    )


@login_required
@lecturer_required
def course_delete(request, slug):
    course = get_object_or_404(Course, slug=slug)
    title = course.title
    program_id = course.program.id
    course.delete()
    messages.success(request, f"Course {title} has been deleted.")
    return redirect("program_detail", pk=program_id)


# ########################################################
# Course Allocation Views
# ########################################################


@method_decorator([login_required, lecturer_required], name="dispatch")
class CourseAllocationFormView(CreateView):
    form_class = CourseAllocationForm
    template_name = "course/course_allocation_form.html"

    def form_valid(self, form):
        lecturer = form.cleaned_data["lecturer"]
        selected_courses = form.cleaned_data["courses"]
        allocation, created = CourseAllocation.objects.get_or_create(lecturer=lecturer)
        allocation.courses.set(selected_courses)
        messages.success(
            self.request, f"Courses allocated to {lecturer.get_full_name} successfully."
        )
        return redirect("course_allocation_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Assign Course"
        return context


@method_decorator([login_required, lecturer_required], name="dispatch")
class CourseAllocationFilterView(FilterView):
    filterset_class = CourseAllocationFilter
    template_name = "course/course_allocation_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Course Allocations"
        return context


@login_required
@lecturer_required
def edit_allocated_course(request, pk):
    allocation = get_object_or_404(CourseAllocation, pk=pk)
    if request.method == "POST":
        form = EditCourseAllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            form.save()
            messages.success(request, "Course allocation has been updated.")
            return redirect("course_allocation_view")
        messages.error(request, "Correct the error(s) below.")
    else:
        form = EditCourseAllocationForm(instance=allocation)
    return render(
        request,
        "course/course_allocation_form.html",
        {"title": "Edit Course Allocation", "form": form},
    )


@login_required
@lecturer_required
def deallocate_course(request, pk):
    allocation = get_object_or_404(CourseAllocation, pk=pk)
    allocation.delete()
    messages.success(request, "Successfully deallocated courses.")
    return redirect("course_allocation_view")


# ########################################################
# File Upload Views
# ########################################################


@login_required
@lecturer_required
def handle_file_upload(request, ref):
    
    course = get_object_or_404(Course, ref=ref)
    if request.method == "POST":
        form = UploadFormFile(request.POST, request.FILES)
        if form.is_valid():
            print("asaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            upload = form.save(commit=False)
            upload.course_id = ref
            upload.save()
            messages.success(request, f"{upload.title} has been uploaded.")
            return redirect("course_detail", ref=ref)
        messages.error(request, "Correct the error(s) below.")
    else:
        form = UploadFormFile()
    return render(
        request,
        "upload/upload_file_form.html",
        {"title": "File Upload", "form": form, "course": course},
    )


@login_required
@lecturer_required
def handle_file_edit(request, slug, file_id):
    course = get_object_or_404(Course, slug=slug)
    upload = get_object_or_404(Upload, pk=file_id)
    if request.method == "POST":
        form = UploadFormFile(request.POST, request.FILES, instance=upload)
        if form.is_valid():
            upload = form.save()
            messages.success(request, f"{upload.title} has been updated.")
            return redirect("course_detail", slug=slug)
        messages.error(request, "Correct the error(s) below.")
    else:
        form = UploadFormFile(instance=upload)
    return render(
        request,
        "upload/upload_file_form.html",
        {"title": "Edit File", "form": form, "course": course},
    )


@login_required
@lecturer_required
def handle_file_delete(request, slug, file_id):
    upload = get_object_or_404(Upload, pk=file_id)
    title = upload.title
    upload.delete()
    messages.success(request, f"{title} has been deleted.")
    return redirect("course_detail", slug=slug)


# ########################################################
# Video Upload Views
# ########################################################


@login_required
@lecturer_required
def handle_video_upload(request, ref):
    course = get_object_or_404(Course, ref=ref)
    if request.method == "POST":
        form = UploadFormVideo(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.course_id = ref
            video.save()
            messages.success(request, f"{video.title} has been uploaded.")
            return redirect("course_detail", ref=ref)
        messages.error(request, "Correct the error(s) below.")
    else:
        form = UploadFormVideo()
    return render(
        request,
        "upload/upload_video_form.html",
        {"title": "Video Upload", "form": form, "course": course},
    )


@login_required
def handle_video_single(request, ref, video_slug):
    print("asdadasdasdasdasdadads",video_slug)
    name = video_slug
    course = get_object_or_404(Course, ref=ref)
    video = get_object_or_404(UploadVideo, slug=name)
    return render(
        request,
        "upload/video_single.html",
        {"video": video, "course": course},
    )


@login_required
@lecturer_required
def handle_video_edit(request, slug, video_slug):
    course = get_object_or_404(Course, slug=slug)
    video = get_object_or_404(UploadVideo, slug=video_slug)
    if request.method == "POST":
        form = UploadFormVideo(request.POST, request.FILES, instance=video)
        if form.is_valid():
            video = form.save()
            messages.success(request, f"{video.title} has been updated.")
            return redirect("course_detail", slug=slug)
        messages.error(request, "Correct the error(s) below.")
    else:
        form = UploadFormVideo(instance=video)
    return render(
        request,
        "upload/upload_video_form.html",
        {"title": "Edit Video", "form": form, "course": course},
    )


@login_required
@lecturer_required
def handle_video_delete(request, ref, video_slug):
    print(ref)
    print(video_slug)
    video = get_object_or_404(UploadVideo, slug=video_slug)
    title = video.title
    video.delete()
    messages.success(request, f"{title} has been deleted.")
    return redirect("course_detail", ref=ref)


# ########################################################
# Course Registration Views
# ########################################################


@login_required
@student_required
def course_registration(request):
    if request.method == "POST":
        student = Student.objects.get(student__pk=request.user.id)
        ids = ()
        data = request.POST.copy()
        data.pop("csrfmiddlewaretoken", None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            course = Course.objects.get(pk=ids[s])
            obj = TakenCourse.objects.create(student=student, course=course)
            obj.save()
        messages.success(request, "Courses registered successfully!")
        return redirect("course_registration")
    else:
        current_semester = Semester.objects.filter(is_current_semester=True).first()
        if not current_semester:
            messages.error(request, "No active semester found.")
            return render(request, "course/course_registration.html")   

        # student = Student.objects.get(student__pk=request.user.id)
        student = get_object_or_404(Student, ref=request.user.student.stud_id)
        taken_courses = TakenCourse.objects.filter(student_id=request.user.student.stud_id)
        t = ()
        for i in taken_courses:
            t += (i.course.pk,)

        courses = (
            Course.objects.filter(
                grade_level=1
            )
        )############
        all_courses = Course.objects.filter(
            grade_level=1 #############
        )

        no_course_is_registered = False  # Check if no course is registered
        all_courses_are_registered = False

        registered_courses = Course.objects.filter(grade_level=1)
        if (
            registered_courses.count() == 0
        ):  # Check if number of registered courses is 0
            no_course_is_registered = True

        if registered_courses.count() == all_courses.count():
            all_courses_are_registered = True

        total_first_semester_credit = 0
        total_sec_semester_credit = 0
        total_registered_credit = 0
        for i in courses:
            # if i.semester == "First":
            total_first_semester_credit += int(1)
            # if i.semester == "Second":
            total_sec_semester_credit += int(1)
        for i in registered_courses:
            total_registered_credit += int(1)
        context = {
            "is_calender_on": True,
            "all_courses_are_registered": all_courses_are_registered,
            "no_course_is_registered": no_course_is_registered,
            "current_semester": current_semester,
            "courses": courses,
            "total_first_semester_credit": total_first_semester_credit,
            "total_sec_semester_credit": total_sec_semester_credit,
            "registered_courses": registered_courses,
            "total_registered_credit": total_registered_credit,
            "student": student,
        }
        return render(request, "course/course_registration.html", context)


@login_required
@student_required
def course_drop(request):
    if request.method == "POST":
        student = get_object_or_404(Student, student__pk=request.user.id)
        course_ids = request.POST.getlist("course_ids")
        print("course_ids", course_ids)
        for course_id in course_ids:
            course = get_object_or_404(Course, pk=course_id)
            TakenCourse.objects.filter(student=student, course=course).delete()
        messages.success(request, "Courses dropped successfully!")
        return redirect("course_registration")


# ########################################################
# User Course List View
# ########################################################


@login_required
def user_course_list(request):
    if request.user.is_lecturer:
        # courses = Course.objects.filter(teacher_id=request.user.lecturer.teacherid)
        section_subquery = Gradelevels.objects.filter(
            ref=OuterRef('grade_level')
        ).values('section')[:1]

        courses = Course.objects.annotate(
            gradelevel_section=Subquery(section_subquery)
        ).filter(teacher_id=request.user.lecturer.teacherid)
        
        for course in courses:
            print(course.sub_name, course.gradelevel_section)

        return render(request, "course/user_course_list.html", {"courses": courses})

    if request.user.is_student:
        student = get_object_or_404(Student, ref=request.user.student.stud_id)
                           
        

        # Query to get subjects related to the student with ref = 1
        # taken_courses = Course.objects.filter(
        #     ref__in=Studentenrollsubject.objects.filter(
        #         sr_id__in=Studentregister.objects.filter(
        #             stud_id=Student.objects.get(ref=request.user.student.stud_id).ref  # Matching stud_id with studentid
        #         ).values('sr_id')
        #     ).values('subject_code')
        # )
        
        taken_courses = Studentenrollsubject.objects.filter(sr__stud_id=request.user.student.stud_id).select_related('sr', 'subject')
        
        
        
        
        # print(taken_courses)
        # print(subjects)
        # taken_courses = Studentenrollsubject.objects.filter(sr_id=student.studentid)
        return render(
            request,
            "course/user_course_list.html",
            {"student": student, "taken_courses": taken_courses},
        )

    # For other users
    return render(request, "course/user_course_list.html")




@login_required
def student_soa(request):
    user_email = request.user.email
    students = []
    selected_student = None
    student_info = {}
    transactions = []
    net_balance = 0.0
    print(user_email)
    
    try:
        
        if request.user.is_student:
            student_ref = request.user.student.stud_id
            students = [request.user.student]
            allowed_refs = [s.ref for s in students]
        else:
            student_ref = request.GET.get('student_ref')            
            parents = Parent.objects.filter(email_address=user_email)
            if not parents.exists():
                return render(request, 'school/error.html', {'message': 'Parent not found.'})
            parent = parents.first()

            parent_students = Parentstudent.objects.filter(gid=parent.pid)
            students = Student.objects.filter(ref__in=[ps.stud_id for ps in parent_students])
            # Filter only if the student_ref is in the list of allowed students
            allowed_refs = [s.ref for s in students]
            print(allowed_refs)
        
        # print(student_ref)
        # print(str(student_ref) in [str(ref) for ref in allowed_refs])
        if str(student_ref) in [str(ref) for ref in allowed_refs]:                           
            if student_ref:
                try:
                    selected_student = Student.objects.get(ref=student_ref)
                except Student.DoesNotExist:
                    selected_student = students.first()
            else:
                selected_student = students.first()

        latest_register = None
        if selected_student:
            latest_register = (
                Studentregister.objects.filter(stud_id=selected_student.ref)
                .annotate(latest_date=Max('dor'))
                .order_by('-latest_date')
                .first()
            )

        if selected_student:
            student_info = {
                'lrn_no': selected_student.lrn_no,
                'name': f"{selected_student.last_name}, {selected_student.first_name} {selected_student.middle_name or ''}",
                'grade': latest_register.grade_level if latest_register else "N/A",
                'voucher': selected_student.if_voucher,
            }

            # Date range
            start_date = '2024-05-08'
            end_date = '2026-12-01'

            # Previous totals
            prev_charges = Scharges.objects.filter(stud_id=selected_student.ref, date__lt=start_date).aggregate(total=Sum('amount'))['total'] or 0
            prev_payments = Spayment.objects.filter(stud_id=selected_student.ref, date__lt=start_date).aggregate(total=Sum('amount'))['total'] or 0
            prev_benefits = Benefits.objects.filter(stud_id=selected_student.ref, date__lt=start_date).aggregate(total=Sum('amount'))['total'] or 0
            prev_balance = prev_charges - (prev_payments + prev_benefits)

            # Previous balance row
            transactions.append({
                'date': datetime.strptime(start_date, "%Y-%m-%d").date(),
                'transaction_type': 'Balance',
                'description': 'Previous Balance',
                'c_amount': prev_charges,
                'p_amount': prev_payments + prev_benefits,
                'balance': prev_balance
            })

            # Current charges
            charges = Scharges.objects.filter(stud_id=selected_student.ref, date__range=[start_date, end_date])
            for c in charges:
                transactions.append({
                    'date': c.date,
                    'transaction_type': 'Charge',
                    'description': c.description,
                    'c_amount': float(c.amount),
                    'p_amount': 0,
                })

            # Current payments
            payments = Spayment.objects.filter(stud_id=selected_student.ref, date__range=[start_date, end_date])
            for p in payments:
                transactions.append({
                    'date': p.date,
                    'transaction_type': 'Payment',
                    'description': p.description,
                    'c_amount': 0,
                    'p_amount': float(p.amount),
                })

            # Current benefits
            benefits = Benefits.objects.filter(stud_id=selected_student.ref, date__range=[start_date, end_date])
            for b in benefits:
                transactions.append({
                    'date': b.date,
                    'transaction_type': 'Benefit',
                    'description': b.description,
                    'c_amount': 0,
                    'p_amount': float(b.amount),
                })

            # Sort and calculate balance
            transactions.sort(key=lambda t: t['date'])
            balance = 0
            for t in transactions:
                balance += t['c_amount'] - t['p_amount']
                t['balance'] = balance

            net_balance = float(balance) if balance is not None else 0.0

            # Format the net_balance as currency
            net_balance = "{:,.2f}".format(net_balance)

    except Exception as e:
        print(f"Error: {e}")

    print(students)
    return render(request, 'course/student_soa.html', {
        'students': students,
        'selected_student': selected_student,
        'student_info': student_info,
        'transactions': transactions,
        'net_balance': net_balance,
    })




# AES Key and IV (must match the server!)
AES_KEY = b"1234567890123456"  # 16 bytes for AES-128
AES_IV = b"6543210987654321"  # 16 bytes for AES-128

def encrypt_message(message: str) -> str:
    """Encrypt the message using AES (CBC mode) and return the base64 encoded encrypted message."""
    
    # Initialize AES cipher in CBC mode with the specified key and IV
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    
    # Pad the message to ensure it's a multiple of the AES block size
    padded_data = pad(message.encode(), AES.block_size)
    
    # Encrypt the padded message
    encrypted_data = cipher.encrypt(padded_data)
    
    # Return the base64 encoded encrypted message
    return b64encode(encrypted_data).decode()


def send_tcp_message_to_vb_server(phone_number, message,  port=5566):
    
    
    sms_settings = get_sms_config()
    host = sms_settings.get('sms_gateway', '127.0.0.1')       
    print(host)
    """Encrypt the message and send it to the VB.NET server over TCP."""
    try:
        encrypted_message = encrypt_message(f"{phone_number} -|- {message}")  # Encrypt the message
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))  # Connect to the server
            s.sendall(encrypted_message.encode())  # Send the encrypted message (already base64 encoded)
            print("Sent via Server:", encrypted_message)
    
    except Exception as e:
        print("TCP Error:", e)
        
        


from django.db import DatabaseError

@login_required
def view_grade(request, course_id):
    course = get_object_or_404(Course, ref=course_id)

    # Get distinct grading periods for the course
    grading_periods = Grade.objects.filter(subject_code=course).values_list('grading_period', flat=True).distinct()

    # Get students enrolled in this course
    enrolled_ids = Studentenrollsubject.objects.filter(subject=course_id).values_list('sr_id', flat=True)
    students_register = Studentregister.objects.filter(sr_id__in=enrolled_ids)
    enrolled_students = Student.objects.filter(ref__in=students_register.values_list('stud_id', flat=True))

    # Build student_grades dictionary
    student_grades = {}
    for student in enrolled_students:
        student_grades[student.ref] = {}
        for period in grading_periods:
            grade = Grade.objects.filter(stud=student, subject_code=course, grading_period=period).first()
            student_grades[student.ref][period] = grade.stud_grade if grade else 'No grade'

    # Handle POST submission
    if request.method == "POST":
        for student in enrolled_students:
            for period in grading_periods:
                field_name = f'grade_{student.ref}_{period}'
                grade_value = request.POST.get(field_name)

                if grade_value:
                    try:
                        grade_value = float(grade_value)  # Validate input
                        grade = Grade.objects.filter(
                            stud=student,
                            subject_code=course,
                            grading_period=period
                        ).first()
                        print(grade)
                        if grade:
                            print("www",grade)
                            # Update existing grade
                            grade.stud_grade = grade_value
                            grading_period=period  # or dynamic
                            grade.gradelevel = 5  # or dynamic                            
                            grade.save()
                        else:
                            print("w22ww",grade)
                            # Insert new grade
                            Grade.objects.create(
                                stud=student,
                                subject_code=course,
                                grading_period=period,
                                stud_grade=grade_value,
                                academic_year='SY. 2025-2026',
                                gradelevel=5
                            )

                    except ValueError:
                        messages.error(request, f"Invalid input for grade of {student} in {period}.")
                    except IntegrityError:
                        messages.error(request, f"Database error when saving grade for {student} in {period}.")

        messages.success(request, "Grades saved successfully!")

        # REFRESH updated grades after POST
    student_grades = {}
    for student in enrolled_students:
        student_grades[student.ref] = {}
        for period in grading_periods:
            grade = Grade.objects.filter(stud=student, subject_code=course, grading_period=period).first()
            student_grades[student.ref][period] = grade.stud_grade if grade else 'No grade'

    
    
    return render(request, 'course/view_grade.html', {
        'course': course,
        'grading_periods': grading_periods,
        'students': enrolled_students,
        'student_grades': student_grades,
    })
    
    
@login_required
def delete_grade(request, student_id, course_id, period):
    try:
        grade = Grade.objects.get(stud_id=student_id, subject_code_id=course_id, grading_period=period)
        print(grade)
        grade.delete()
        messages.success(request, "Grade deleted successfully.")
    except Grade.DoesNotExist:
        messages.error(request, "Grade not found.")

    return redirect('view_grade', course_id=course_id)
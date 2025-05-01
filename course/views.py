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


from accounts.decorators import lecturer_required, student_required
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
    Course,
    CourseAllocation,
    Program,
    Upload,
    UploadVideo,
)

from course.importmodels import (
    Subject,
    Gradelevels,
    Studentregister,
    Studentenrollsubject,
    Teacher,
    Attendance,
    Student,
    Parent,
    Parentstudent,
    Scharges,
    Spayment
)
from result.models import TakenCourse


# ########################################################
# Program Views
# ########################################################


@method_decorator([login_required, lecturer_required], name="dispatch")
class ProgramFilterView(FilterView):
    filterset_class = GradelevelsFilter
    template_name = "course/program_list.html"

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
    courses = Subject.objects.filter(grade_level=pk)
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
    enrolled_ids = Studentenrollsubject.objects.filter(subject_code=course_id).values_list('sr_id', flat=True)

    # Get all students register entries
    students_register = Studentregister.objects.filter(sr_id__in=enrolled_ids)
    
    # Get all students from Student table
    students = Student.objects.filter(ref__in=students_register.values_list('stud_id', flat=True))
    
    course = get_object_or_404(Subject, ref=course_id)    
    
    
    # print(course_id)
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
        
        course = get_object_or_404(Subject, ref=course_id)

        # Fetch enrolled students
        enrolled_ids = Studentenrollsubject.objects.filter(subject_code=course_id).values_list('sr_id', flat=True)
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
    course = get_object_or_404(Subject, ref=ref)
    files = Upload.objects.filter(course_id="1")
   
    videos = UploadVideo.objects.filter(course_id=ref)
    lecturers = Teacher.objects.get(teacher_id=course.teacher_id)
    
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
    
    course = get_object_or_404(Subject, ref=ref)
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
    course = get_object_or_404(Subject, ref=ref)
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
    course = get_object_or_404(Subject, ref=ref)
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
def handle_video_delete(request, slug, video_slug):
    video = get_object_or_404(UploadVideo, slug=video_slug)
    title = video.title
    video.delete()
    messages.success(request, f"{title} has been deleted.")
    return redirect("course_detail", slug=slug)


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
        student = get_object_or_404(Student, student__id=request.user.id)
        taken_courses = TakenCourse.objects.filter(student__student__id=request.user.id)
        t = ()
        for i in taken_courses:
            t += (i.course.pk,)

        courses = (
            Course.objects.filter(
                program__pk=student.program.id,
                level=student.level,
                semester=current_semester,
            )
            .exclude(id__in=t)
            .order_by("year")
        )
        all_courses = Course.objects.filter(
            level=student.level, program__pk=student.program.id
        )

        no_course_is_registered = False  # Check if no course is registered
        all_courses_are_registered = False

        registered_courses = Course.objects.filter(level=student.level).filter(id__in=t)
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
            if i.semester == "First":
                total_first_semester_credit += int(i.credit)
            if i.semester == "Second":
                total_sec_semester_credit += int(i.credit)
        for i in registered_courses:
            total_registered_credit += int(i.credit)
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
        courses = Subject.objects.filter(teacher_id=request.user.lecturer.teacherid)
        return render(request, "course/user_course_list.html", {"courses": courses})

    if request.user.is_student:
        student = get_object_or_404(Student, ref="1")                   
        

        # Query to get subjects related to the student with ref = 1
        taken_courses = Subject.objects.filter(
            ref__in=Studentenrollsubject.objects.filter(
                sr_id__in=Studentregister.objects.filter(
                    stud_id=Student.objects.get(ref=1).ref  # Matching stud_id with studentid
                ).values('sr_id')
            ).values('subject_code')
        )

        # print(subjects)
        # taken_courses = Studentenrollsubject.objects.filter(sr_id=student.studentid)
        return render(
            request,
            "course/user_course_list.html",
            {"student": student, "taken_courses": taken_courses},
        )

    # For other users
    return render(request, "course/user_course_list.html")





def student_soa(request):
    user_email = request.user.email
    students = []
    selected_student = None
    student_info = {}
    transactions = []
    net_balance = 0.0
    
    try:
        # Fetch parent based on user email
        parents = Parent.objects.filter(email_address=user_email)        
        if not parents.exists():
            print("Parent not found for the given email.")
            return render(request, 'school/error.html', {'message': 'Parent not found.'})

        parent = parents.first()  # Select the first parent if multiple exist for now

        # Fetch associated students
        parent_students = Parentstudent.objects.filter(gid=parent.pid)

        if parent_students.exists():
            students = Student.objects.filter(ref__in=[ps.stud_id for ps in parent_students])
            if students.exists():
                print("Students found:", students)
            else:
                print("No students found for this parent.")
        else:
            print("No student records associated with this parent.")

        # Get the selected student from the GET request
        student_ref = request.GET.get('student_ref')
        print(student_ref)
        # If there's a selected student, filter by the selected student reference
        if student_ref:
            selected_student = students.get(ref=student_ref)  # This will raise an exception if not found
            print("Selected student:", selected_student)
        else:
            selected_student = students.first()  # Set the first student as default if none selected

        # Fetch the latest Studentregister data for the selected student
        latest_register = None
        if selected_student:
            latest_register = (
                Studentregister.objects.filter(stud_id=selected_student.ref)
                .annotate(latest_date=Max('dor'))  # Replace 'dor' with the correct field name
                .order_by('-latest_date')
                .first()
            )
            print("Latest register:", latest_register)

        # Prepare student information including grade level from Studentregister
        if selected_student:
            student_info = {
                'lrn_no': selected_student.lrn_no,
                'name': f"{selected_student.last_name}, {selected_student.first_name} {selected_student.middle_name or ''}",
                'grade': latest_register.grade_level if latest_register else "N/A",
                'voucher': selected_student.if_voucher,
            }

            # Retrieve charges and payments
            start_date = '2024-06-01'
            end_date = '2026-12-01'

            queryset_charges = Scharges.objects.filter(stud_id=selected_student.ref, date__range=[start_date, end_date])
            queryset_payments = Spayment.objects.filter(stud_id=selected_student.ref, date__range=[start_date, end_date])

            # Combine and prepare transactions for display
            charges = queryset_charges.annotate(
                c_amount=F('amount'),
                p_amount=Value(0),
                transaction_type=Value('Charge')
            )
            payments = queryset_payments.annotate(
                c_amount=Value(0),
                p_amount=F('amount'),
                transaction_type=Value('Payment')
            )

            transactions = sorted(
                list(charges) + list(payments),
                key=lambda t: t.date
            )

            # Calculate running balance
            balance = 0
            for transaction in transactions:
                balance += transaction.c_amount - transaction.p_amount
                transaction.balance = balance

            # Set the final net balance
            net_balance = balance

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        
    # Return the data to the template
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
        
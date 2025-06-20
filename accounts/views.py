from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template, render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django_filters.views import FilterView
from xhtml2pdf import pisa
from django.views.decorators.http import require_GET
from accounts.decorators import admin_required
from accounts.filters import LecturerFilter, StudentFilter, ParentFilter
from accounts.forms import (
    ParentAddForm,
    ProfileUpdateForm,
    ProgramUpdateForm,
    StaffAddForm,
    StudentAddForm,  
    LecturerOnlyForm,
    StudentinfoForm
    
)

from io import TextIOWrapper
import csv

from accounts.models import Parent, Student, User, Lecturer
from core.models import Semester, Session
from django.db.models import Sum
from core.fastfood_models import TblAcc, TblPos

from course.importmodels import Student as Studentinfo

# from course.models import Course
from result.models import TakenCourse
from django.db.models import OuterRef, Subquery
from course.importmodels import (
    Subject as Course,
    Gradelevels,
    Studentenrollsubject,
    License,
    Parent as Parentinfo
)



# ########################################################
# Utility Functions
# ########################################################


def render_to_pdf(template_name, context):
    """Render a given template to PDF format."""
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="profile.pdf"'
    template = render_to_string(template_name, context)
    pdf = pisa.CreatePDF(template, dest=response)
    if pdf.err:
        return HttpResponse("We had some problems generating the PDF")
    return response


# ########################################################
# Authentication and Registration
# ########################################################


def validate_username(request):
    username = request.GET.get("username", None)
    data = {"is_taken": User.objects.filter(username__iexact=username).exists()}
    return JsonResponse(data)


def register(request):
    if request.method == "POST":
        form = StudentAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect("login")
        messages.error(
            request, "Something is not correct, please fill all fields correctly."
        )
    else:
        form = StudentAddForm()
    return render(request, "registration/register.html", {"form": form})


# ########################################################
# Profile Views
# ########################################################


@login_required
def profile(request):
    """Show profile of the current user."""    
    current_session = Session.objects.filter(is_current_session=True).first()
    current_semester = Semester.objects.filter(
        is_current_semester=True, session=current_session
    ).first()

    context = {
        "title": request.user.get_full_name,
        "current_session": current_session,
        "current_semester": current_semester,
    }

    if request.user.is_lecturer:
        # courses = Course.objects.filter(
        #     teacher_id=request.user.lecturer.teacherid
        # )
        
        
        section_subquery = Gradelevels.objects.filter(
            ref=OuterRef('grade_level')
        ).values('section')[:1]
        
        courses = Course.objects.annotate(
            gradelevel_section=Subquery(section_subquery)
        ).filter(teacher_id=request.user.lecturer.teacherid)
        
        
        
        
        print(courses)
        context["courses"] = courses
        return render(request, "accounts/profile.html", context)

    if request.user.is_student:
        student = get_object_or_404(Student, student__pk=request.user.id)  
         
        studentinfo = get_object_or_404(Studentinfo, ref=student.stud_id)   
        studschool = studentinfo.rfid

        print(studschool)
        
        if student:
            total_balance = TblAcc.objects.using('caf_db').filter(stud_id=studschool).aggregate(total=Sum('balance'))['total'] or 0
            total_pos = TblPos.objects.using('caf_db').filter(customerid=studschool).aggregate(total=Sum('grandtotal'))['total'] or 0
            
            net = total_balance - total_pos
            print(net)
        else:
            print("Student not found.")
        
   
        
        courses = TakenCourse.objects.filter(
            student_id=request.user.student.stud_id
        )
        context.update(
            {
                # ""parent": parent,"
                "courses": courses,
                "level": student.level,
                 "Cafeteria": net,
            }
        )
        return render(request, "accounts/profile.html", context)


    # For superuser or other staff
    staff = User.objects.filter(is_lecturer=True)
    context["staff"] = staff
    return render(request, "accounts/profile.html", context)


@login_required
@admin_required
def profile_single(request, user_id):
    """Show profile of any selected user."""
    if request.user.id == user_id:
        return redirect("profile")

    current_session = Session.objects.filter(is_current_session=True).first()
    current_semester = Semester.objects.filter(
        is_current_semester=True, session=current_session
    ).first()
    user = get_object_or_404(User, pk=user_id)

    context = {
        "title": user.get_full_name,
        "user": user,
        "current_session": current_session,
        "current_semester": current_semester,
    }

    if user.is_lecturer:
        
        
        section_subquery = Gradelevels.objects.filter(
            ref=OuterRef('grade_level')
        ).values('section')[:1]
        
        courses = Course.objects.annotate(
            gradelevel_section=Subquery(section_subquery)
        ).filter(teacher_id=user.lecturer.teacherid)
        print(courses)
        
        context.update(
            {
                "user_type": "Lecturer",
                "courses": courses,
            }
        )
    elif user.is_student:
        print(user.is_student)
        student = get_object_or_404(Student, student__pk=user_id)
        # courses = TakenCourse.objects.filter(
        #     student__student__id=user_id
        # )
        
        courses = Studentenrollsubject.objects.filter(sr__stud_id=student.stud_id).select_related('sr', 'subject')
        
        
        context.update(
            {
                "user_type": "Student",
                "courses": courses,
                "student": student,
            }
        )
    else:
        context["user_type"] = "Superuser"

    if request.GET.get("download_pdf"):
        return render_to_pdf("pdf/profile_single.html", context)

    return render(request, "accounts/profile_single.html", context)


@login_required
@admin_required
def admin_panel(request):
    return render(request, "setting/admin_panel.html", {"title": "Admin Panel"})


# ########################################################
# Settings Views
# ########################################################


@login_required
def profile_update(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")
        messages.error(request, "Please correct the error(s) below.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "setting/profile_info_change.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("profile")
        messages.error(request, "Please correct the error(s) below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "setting/password_change.html", {"form": form})


# ########################################################
# Staff (Lecturer) Views
# ########################################################


@login_required
@admin_required
def staff_add_view(request):
    if request.method == "POST":
        form = StaffAddForm(request.POST)
        if form.is_valid():
            lecturer = form.save()
            full_name = lecturer.get_full_name
            email = lecturer.email
            messages.success(
                request,
                f"Account for lecturer {full_name} has been created. "
                f"An email with account credentials will be sent to {email} within a minute.",
            )
            return redirect("lecturer_list")
    else:
        form = StaffAddForm()
    return render(
        request, "accounts/add_staff.html", {"title": "Add Lecturer", "form": form}
    )


@login_required
@admin_required
def edit_staff(request, pk):
    lecturer = get_object_or_404(User, is_lecturer=True, pk=pk)
    lecturer1 = get_object_or_404(Lecturer, user=lecturer)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=lecturer)
        lecturer_form = LecturerOnlyForm(request.POST, instance=lecturer1)
        if form.is_valid() and lecturer_form.is_valid():
            form.save()
            lecturer_form.save()
            
            full_name = lecturer.get_full_name
            messages.success(request, f"Lecturer {full_name} has been updated.")
            return redirect("lecturer_list")
        messages.error(request, "Please correct the error below.")
    else:
        form = ProfileUpdateForm(instance=lecturer)
        lecturer_form = LecturerOnlyForm(instance=lecturer1)

    current_teacher = lecturer1.teacherid if lecturer1.teacherid else None
    

    return render(
        request,
        "accounts/edit_lecturer.html",
        {
            "title": "Edit Lecturer",
            "form": form,
            "lecturer_form": lecturer_form,
            "current_teacher": current_teacher,
        }
    )




@method_decorator([login_required, admin_required], name="dispatch")
class LecturerFilterView(FilterView):
    filterset_class = LecturerFilter
    queryset = User.objects.filter(is_lecturer=True)
    template_name = "accounts/lecturer_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Lecturers"
        return context


@login_required
@admin_required
def render_lecturer_pdf_list(request):
    lecturers = User.objects.filter(is_lecturer=True)
    template_path = "pdf/lecturer_list.html"
    context = {"lecturers": lecturers}
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="lecturers_list.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse(f"We had some errors <pre>{html}</pre>")
    return response


@login_required
@admin_required
def delete_staff(request, pk):
    lecturer = get_object_or_404(User, is_lecturer=True, pk=pk)
    full_name = lecturer.get_full_name
    lecturer.delete()
    messages.success(request, f"Lecturer {full_name} has been deleted.")
    return redirect("lecturer_list")


# ########################################################
# Student Views
# ########################################################


@admin_required
def student_add_view(request):
    if request.method == "POST":
        form = StudentAddForm(request.POST)
        if form.is_valid():
            student = form.save()
            full_name = student.get_full_name
            email = student.email
            messages.success(
                request,
                f"Account for {full_name} has been created. "
                f"An email with account credentials will be sent to {email} within a minute.",
            )
            return redirect("student_list")
        messages.error(request, "Correct the error(s) below.")
    else:
        form = StudentAddForm()
    return render(
        request, "accounts/add_student.html", {"title": "Add Student", "form": form}
    )



def bulk_upload_students(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        print("asdadsasd")
        with transaction.atomic():
            for row in reader:
                if User.objects.filter(username=row['username']).exists():
                    continue  # Skip existing users

                user = User.objects.create_user(
                    username=row['username'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    password=row['password'],
                )
                user.is_student = True
                user.gender = row['gender']
                user.address = row['address']
                user.phone = row['phone']
                user.save()

                # Get foreign keys
                program = Program.objects.filter(pk=row['program']).first()
                stud2 = Student2.objects.filter(ref=row['studid']).first()

                if not stud2:
                    messages.error(request, f"Student2 with ref {row['studid']} not found.")
                    continue

                Student.objects.create(
                    student=user,
                    level=row['level'],
                    program=program,
                    stud_id=stud2.ref,
                )

        messages.success(request, "Bulk student upload completed.")
        return redirect('student_list')

    return render(request, 'accounts/bulk_upload.html', {"title": "Bulk Upload Students"})


@login_required
@admin_required
def edit_student(request, pk):
    student_user = get_object_or_404(User, is_student=True, pk=pk)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=student_user)
        
        if form.is_valid():
            form.save()
            full_name = student_user.get_full_name
            messages.success(request, f"Student {full_name} has been updated.")
            return redirect("student_list")
        messages.error(request, "Please correct the error below.")
    else:
        form = ProfileUpdateForm(instance=student_user)
    return render(
        request, "accounts/edit_student.html", {"title": "Edit Student", "form": form}
    )


@method_decorator([login_required, admin_required], name="dispatch")
class StudentListView(FilterView):
    queryset = Student.objects.all()
    filterset_class = StudentFilter
    template_name = "accounts/student_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Students"
        return context

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('csv_file')

        if not csv_file:
            messages.error(request, "No file uploaded.")
            return redirect(request.path)

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please upload a valid CSV file.")
            return redirect(request.path)

        try:
            decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.DictReader(decoded_file)

            success_count = 0
            skipped_count = 0

            for row in reader:
                username = row.get('username', '').strip()
                email = row.get('email', '').strip()
                print(username)
                if not username or not email:
                    skipped_count += 1
                    continue  # Required fields missing

                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': row.get('first_name', '').strip(),
                        'last_name': row.get('last_name', '').strip(),
                        'email': email,
                        'is_student' : 1,
                        'address': row.get('address', ''),
                        'phone': row.get('phone', ''),
                    }                    
                )
                
                

                # Set password if user was created
                if created:
                    user.set_password(row.get('password') or "default123")
                    user.save()

                Student.objects.update_or_create(
                    student=user,
                    defaults={
                        # 'address': row.get('address', ''),
                        # 'phone': row.get('phone', ''),
                        # 'gender': row.get('gender', ''),
                        # 'level': row.get('level', 1),
                        # 'program': row.get('program', 1),
                        'stud_id': row.get('studid', ''),
                    }
                )

                success_count += 1

            messages.success(request, f"Imported {success_count} students. Skipped {skipped_count} invalid rows.")
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")

        return redirect(request.path)

@login_required
@admin_required
def render_student_pdf_list(request):
    students = Student.objects.all()
    template_path = "pdf/student_list.html"
    context = {"students": students}
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="students_list.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse(f"We had some errors <pre>{html}</pre>")
    return response


@login_required
@admin_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    full_name = student.student.get_full_name
    student.delete()
    messages.success(request, f"Student {full_name} has been deleted.")
    return redirect("student_list")


@login_required
@admin_required
def edit_student_program(request, pk):
    student = get_object_or_404(Student, student_id=pk)
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = ProgramUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            full_name = user.get_full_name
            messages.success(request, f"{full_name}'s program has been updated.")
            return redirect("profile_single", user_id=pk)
        messages.error(request, "Please correct the error(s) below.")
    else:
        form = ProgramUpdateForm(instance=student)
    return render(
        request,
        "accounts/edit_student_program.html",
        {"title": "Edit Program", "form": form, "student": student},
    )


# ########################################################
# Parent Views
# ########################################################


# @method_decorator([login_required, admin_required], name="dispatch")
# class ParentAdd(CreateView):
#     model = Parent
#     form_class = ParentAddForm
#     template_name = "accounts/parent_form.html"

#     def form_valid(self, form):
#         messages.success(self.request, "Parent added successfully.")
#         return super().form_valid(form)



def ParentAdd(request):
    if request.method == "POST":
        form = ParentAddForm(request.POST)
        if form.is_valid():
            parent = form.save()
            full_name = parent.get_full_name
            email = parent.email
            messages.success(
                request,
                f"Account for {full_name} has been created. "
                f"An email with account credentials will be sent to {email} within a minute.",
            )
            return redirect("parents_list")
        messages.error(request, "Correct the error(s) below.")
    else:
        form = ParentAddForm()
    return render(
        request, "accounts/parent_form.html", {"title": "Add Student", "form": form}
    )   



@method_decorator([login_required, admin_required], name="dispatch")
class ParentListView(FilterView):
    queryset = User.objects.filter(is_parent=True)
    filterset_class = ParentFilter    
    template_name = "accounts/parent_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Parents"
        return context
    
    
# @method_decorator([login_required, admin_required], name="dispatch")
# class LecturerFilterView(FilterView):
#     filterset_class = LecturerFilter
#     queryset = User.objects.filter(is_lecturer=True)
#     template_name = "accounts/lecturer_list.html"
#     paginate_by = 10

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Lecturers"
#         return context    
    
    


@login_required
@admin_required
def edit_parent(request, pk):
    parent_user = get_object_or_404(User, is_parent=True, pk=pk)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=parent_user)
        
        if form.is_valid():
            form.save()
            full_name = parent_user.get_full_name
            messages.success(request, f"parent {full_name} has been updated.")
            return redirect("parents_list")
        messages.error(request, "Please correct the error below.")
    else:
        form = ProfileUpdateForm(instance=parent_user)
    return render(
        request, "accounts/edit_parent.html", {"title": "Edit parent", "form": form}
    )
    
    
    

@login_required
@admin_required
def delete_parent(request, pk):
    parent = get_object_or_404(User, is_parent=True, pk=pk)
    full_name = parent.get_full_name
    parent.delete()
    messages.success(request, f"parent {full_name} has been deleted.")
    return redirect("parents_list")



@require_GET
def activation(request, license_key):
    try:
        license = License.objects.get(lisense=license_key)
        return JsonResponse({
            "status": "success",
            "license_key": license_key,
            "validated_date": license.dateended.isoformat()
        })
    except License.DoesNotExist:
        return JsonResponse({
            "status": "fail",
            "message": "Invalid license key"
        }, status=404)
        
        
        
def student_register(request):
    if request.method == 'POST':
        form = StudentinfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Update with your success page
    else:
        form = StudentinfoForm()
    return render(request, 'accounts/registration.html', {'form': form})
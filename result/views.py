from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from collections import defaultdict
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

# from reportlab.platypus.tables import Table
from reportlab.lib.units import inch
from reportlab.lib import colors

from core.models import Session, Semester
# from course.models import Course
from accounts.models import Student
from accounts.decorators import lecturer_required, student_required, parent_required
from .models import TakenCourse, Result

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
    Grade
)


CM = 2.54


# ########################################################
# Score Add & Add for
# ########################################################
@login_required
@lecturer_required
def add_score(request):
    """
    Shows a page where a lecturer will select a course allocated
    to him for score entry. in a specific semester and session
    """
    current_session = Session.objects.filter(is_current_session=True).first()
    current_semester = Semester.objects.filter(
        is_current_semester=True, session=current_session
    ).first()

    if not current_session or not current_semester:
        messages.error(request, "No active semester found.")
        return render(request, "result/add_score.html")

    # semester = Course.objects.filter(
    # allocated_course__lecturer__pk=request.user.id,
    # semester=current_semester)
    courses = Course.objects.filter(
        teacher_id=request.user.lecturer.teacherid
    )
    context = {
        "current_session": current_session,
        "current_semester": current_semester,
        "courses": courses,
    }
    return render(request, "result/add_score.html", context)


@login_required
@lecturer_required
def add_score_for(request, id):
    """
    Shows a page where a lecturer will add score for students that
    are taking courses allocated to him in a specific semester and session
    """
    current_session = Session.objects.get(is_current_session=True)
    current_semester = get_object_or_404(
        Semester, is_current_semester=True, session=current_session
    )
    if request.method == "GET":
        courses = Course.objects.filter(
            teacher_id=request.user.lecturer.teacherid
        )
        course = Course.objects.get(pk=id)
        # myclass = Class.objects.get(lecturer__pk=request.user.id)
        # myclass = get_object_or_404(Class, lecturer__pk=request.user.id)

        # students = TakenCourse.objects.filter(
        # course__allocated_course__lecturer__pk=request.user.id).filter(
        #  course__id=id).filter(
        #  student__allocated_student__lecturer__pk=request.user.id).filter(
        #  course__semester=current_semester)
        
        
        # students = (
        #     TakenCourse.objects.filter(
        #         course__allocated_course__lecturer__pk=request.user.id
        #     )
        #     .filter(course__id=id)
        #     .filter(course__semester=current_semester)
        # )
        
        
        enrolled_ids = Studentenrollsubject.objects.filter(subject_code=id).values_list('sr_id', flat=True)
        students_register = Studentregister.objects.filter(sr_id__in=enrolled_ids)
        students = Student.objects.filter(ref__in=students_register.values_list('stud_id', flat=True))
        
        
        context = {
            "title": "Submit Score",
            "courses": courses,
            "course": course,
            # "myclass": myclass,
            "students": students,
            "current_session": current_session,
            "current_semester": current_semester,
        }
        return render(request, "result/add_score_for.html", context)

    if request.method == "POST":
        ids = ()
        data = request.POST.copy()        
        data.pop("csrfmiddlewaretoken", None)  # remove csrf_token
        
        for key in data.keys():
            
            ids = ids + (
                str(key),
            )  # gather all the all students id (i.e the keys) in a tuple
        print(ids)    
        for s in range(
            0, len(ids)
        ):  # iterate over the list of student ids gathered above
            
            # student = TakenCourse.objects.get(id=ids[s])
            try:
                student = TakenCourse.objects.get(id=ids[s])
            except TakenCourse.DoesNotExist:
                print(f"TakenCourse with ID {ids[s]} does not exist. Skipping.")
                continue
            
            
            # print(student)
            # print(student.student)
            # print(student.student.program.id)
            
            # courses = (
            #     Course.objects.filter(level=student.student.level)
            #     .filter(program__pk=student.student.program.id)
            #     .filter(semester=current_semester)
            # )  # all courses of a specific level in current semester
            
            # Step 1: Get all subject_code and sr_id combinations from Studentenrollsubject
            enrollments = Studentenrollsubject.objects.all()

            # Step 2: Get subject refs from enrollments
            subject_codes = enrollments.values_list('subject_code', flat=True)
            sr_ids = enrollments.values_list('sr_id', flat=True)

            # Step 3: Fetch related studentregister records
            student_registers = Studentregister.objects.filter(sr_id__in=sr_ids)

            # Step 4: Fetch related subject records
            courses = Course.objects.filter(ref__in=subject_codes)

            
            
            
            total_credit_in_semester = 0
            for i in courses:
                if i == courses.count():
                    break
                total_credit_in_semester += int(1) ###############
            score = data.getlist(
                ids[s]
            )  # get list of score for current student in the loop
            assignment = score[
                0
            ]  # subscript the list to get the fisrt value > ca score
            mid_exam = score[1]  # do the same for exam score
            quiz = score[2]
            attendance = score[3]
            final_exam = score[4]
            obj = TakenCourse.objects.get(pk=ids[s])  # get the current student data
            obj.assignment = assignment  # set current student assignment score
            obj.mid_exam = mid_exam  # set current student mid_exam score
            obj.quiz = quiz  # set current student quiz score
            obj.attendance = attendance  # set current student attendance score
            obj.final_exam = final_exam  # set current student final_exam score

            obj.total = obj.get_total()
            obj.grade = obj.get_grade()

            # obj.total = obj.get_total(assignment, mid_exam, quiz, attendance, final_exam)
            # obj.grade = obj.get_grade(assignment, mid_exam, quiz, attendance, final_exam)

            obj.point = obj.get_point()
            obj.comment = obj.get_comment()
            # obj.carry_over(obj.grade)
            # obj.is_repeating()
            
            print("aaaaaaaaaaaaaaaaaaaaaaaa")
            obj.save()
            gpa = obj.calculate_gpa()
            cgpa = obj.calculate_cgpa()

            try:
                a = Result.objects.get(
                    student=student.student,
                    semester=current_semester,
                    session=current_session,
                    level=1,############
                )
                a.gpa = gpa
                a.cgpa = cgpa
                a.save()
            except:
                Result.objects.get_or_create(
                    student=student.student,
                    gpa=gpa,
                    semester=current_semester,
                    session=current_session,
                     level=1,############
                )

            # try:
            #     a = Result.objects.get(student=student.student,
            # semester=current_semester, level=student.student.level)
            #     a.gpa = gpa
            #     a.cgpa = cgpa
            #     a.save()
            # except:
            #     Result.objects.get_or_create(student=student.student, gpa=gpa,
            # semester=current_semester, level=student.student.level)

        messages.success(request, "Successfully Recorded! ")
        return HttpResponseRedirect(reverse_lazy("add_score_for", kwargs={"id": id}))
    return HttpResponseRedirect(reverse_lazy("add_score_for", kwargs={"id": id}))


# ########################################################

@login_required
def grade_result(request):
    user_email = request.user.email
    student_ref = request.GET.get('student_ref')
    selected_student = None
    students = []
    print(student_ref)
    if request.user.is_student:
        student_ref = request.user.student.stud_id
        # students = Student.objects.get(ref=studeyynt_ref)#[request.user.student]
        students = [Student.objects.get(ref=student_ref)]

    else:
        parents = Parent.objects.filter(email_address=user_email)
        if not parents.exists():
            return render(request, 'school/error.html', {'message': 'Parent not found.'})
        parent = parents.first()

        parent_students = Parentstudent.objects.filter(gid=parent.pid)
        students = Student.objects.filter(ref__in=[ps.stud_id for ps in parent_students])

    if student_ref:
        try:
            selected_student = Student.objects.get(ref=student_ref)
        except Student.DoesNotExist:
            selected_student = students.first()
    else:
        selected_student = students.first()
    
        
        
    # Fetching courses and grades for the selected student
    courses = Studentenrollsubject.objects.filter(sr__stud_id=selected_student.ref).select_related('sr', 'subject')
    
    grades = Grade.objects.filter(
        stud=selected_student.ref,
        subject_code__in=[c.subject for c in courses]
    )
    print(grades)
    grading_periods = grades.values_list('grading_period', flat=True).distinct()
    grade_dict = {}
    for g in grades:
        key = (g.subject_code.ref, g.grading_period)
        grade_dict[key] = g.stud_grade

    results = Result.objects.filter(student_id=selected_student.ref)
    
    # Group results by academic year
    academic_years = {}
    for result in results:
        academic_year = result.session.split('-')[0]
        if academic_year not in academic_years:
            academic_years[academic_year] = []
        academic_years[academic_year].append(result)

    # Sorting the academic years
    sorted_academic_years = sorted(academic_years.items())
    
    total_first_semester_credit = 0
    total_sec_semester_credit = 0
    for i in courses:
        total_first_semester_credit += 1
        total_sec_semester_credit += 1

    previousCGPA = 0
    for i in results:
        previousLEVEL = i.level
        try:
            a = Result.objects.get(
                student__student__pk=request.user.id,
                level=previousLEVEL,
                semester="Second",
            )
            previousCGPA = a.cgpa
            break
        except:
            previousCGPA = 0
            
    print(students)
    context = {
        "courses": courses,
        'grade_dict': grade_dict,
        'grading_periods': grading_periods,
        "results": results,
        "academic_years": sorted_academic_years,  # Pass the academic years to the template
        "student": selected_student,
        "students": students,  # Pass students to the template for dropdown
        "total_first_semester_credit": total_first_semester_credit,
        "total_sec_semester_credit": total_sec_semester_credit,
        "total_first_and_second_semester_credit": total_first_semester_credit + total_sec_semester_credit,
        "previousCGPA": previousCGPA,
    }

    return render(request, "result/grade_results.html", context)


@login_required
@student_required
def assessment_result(request):
    student = Student.objects.get(ref=request.user.student.stud_id)
    courses = TakenCourse.objects.filter(
        student_id=request.user.id
    )
    result = Result.objects.filter(student_id=request.user.student.stud_id)

    context = {
        "courses": courses,
        "result": result,
        "student": student,
    }

    return render(request, "result/assessment_results.html", context)


@login_required
@lecturer_required
def result_sheet_pdf_view(request, id):
    current_semester = Semester.objects.get(is_current_semester=True)
    current_session = Session.objects.get(is_current_session=True)
    result = TakenCourse.objects.filter(course_id=id)
    
    
    course = get_object_or_404(Course, ref=id)
    no_of_pass = TakenCourse.objects.filter(course__pk=id, comment="PASS").count()
    no_of_fail = TakenCourse.objects.filter(course__pk=id, comment="FAIL").count()
    fname = (
        str(current_semester)
        + "_semester_"
        + str(current_session)
        + "_"
        + str(course)
        + "_resultSheet.pdf"
    )
    fname = fname.replace("/", "-")
    flocation = settings.MEDIA_ROOT + "/result_sheet/" + fname

    doc = SimpleDocTemplate(
        flocation,
        rightMargin=0,
        leftMargin=6.5 * CM,
        topMargin=0.3 * CM,
        bottomMargin=0,
    )
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(name="ParagraphTitle", fontSize=11, fontName="FreeSansBold")
    )
    Story = [Spacer(1, 0.2)]
    style = styles["Normal"]

    # picture = request.user.picture
    # l_pic = Image(picture, 1*inch, 1*inch)
    # l_pic.__setattr__("_offs_x", 200)
    # l_pic.__setattr__("_offs_y", -130)
    # Story.append(l_pic)

    # logo = settings.MEDIA_ROOT + "/logo/logo-mini.png"
    # im_logo = Image(logo, 1*inch, 1*inch)
    # im_logo.__setattr__("_offs_x", -218)
    # im_logo.__setattr__("_offs_y", -60)
    # Story.append(im_logo)

    print("\nsettings.MEDIA_ROOT", settings.MEDIA_ROOT)
    print("\nsettings.STATICFILES_DIRS[0]", settings.STATICFILES_DIRS[0])
    logo = settings.STATICFILES_DIRS[0] + "/img/brand.png"
    im = Image(logo, 1 * inch, 1 * inch)
    im.__setattr__("_offs_x", -200)
    im.__setattr__("_offs_y", -45)
    Story.append(im)

    style = getSampleStyleSheet()
    normal = style["Normal"]
    normal.alignment = TA_CENTER
    normal.fontName = "Helvetica"
    normal.fontSize = 12
    normal.leading = 15
    title = (
        "<b> "
        + str(current_semester)
        + " Semester "
        + str(current_session)
        + " Result Sheet</b>"
    )
    title = Paragraph(title.upper(), normal)
    Story.append(title)
    Story.append(Spacer(1, 0.1 * inch))

    style = getSampleStyleSheet()
    normal = style["Normal"]
    normal.alignment = TA_CENTER
    normal.fontName = "Helvetica"
    normal.fontSize = 10
    normal.leading = 15
    title = "<b>Course lecturer: " + request.user.get_full_name + "</b>"
    title = Paragraph(title.upper(), normal)
    Story.append(title)
    Story.append(Spacer(1, 0.1 * inch))

    normal = style["Normal"]
    normal.alignment = TA_CENTER
    normal.fontName = "Helvetica"
    normal.fontSize = 10
    normal.leading = 15
    level = result.filter(course_id=id).first()
    title = "<b>Level: </b>" + str(course.grade_level)
    title = Paragraph(title.upper(), normal)
    Story.append(title)
    Story.append(Spacer(1, 0.6 * inch))

    elements = []
    count = 0
    header = [("S/N", "ID NO.", "FULL NAME", "TOTAL", "GRADE", "POINT", "COMMENT")]

    table_header = Table(header, [inch], [0.5 * inch])
    table_header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.black),
                ("TEXTCOLOR", (1, 0), (-1, -1), colors.white),
                ("TEXTCOLOR", (0, 0), (0, 0), colors.cyan),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    Story.append(table_header)

    for student in result:
        data = [
            (
                count + 1,
                student.student_id,
                student.student_id,
                # Paragraph(
                #     student.student_id, styles["Normal"]
                # ),
                student.total,
                student.grade,
                student.point,
                student.comment,
            )
        ]
        color = colors.black
        if student.grade == "F":
            color = colors.red
        count += 1

        t_body = Table(data, colWidths=[inch])
        t_body.setStyle(
            TableStyle(
                [
                    ("INNERGRID", (0, 0), (-1, -1), 0.05, colors.black),
                    ("BOX", (0, 0), (-1, -1), 0.1, colors.black),
                ]
            )
        )
        Story.append(t_body)

    Story.append(Spacer(1, 1 * inch))
    style_right = ParagraphStyle(
        name="right", parent=styles["Normal"], alignment=TA_RIGHT
    )
    tbl_data = [
        [
            Paragraph("<b>Date:</b>_____________________________", styles["Normal"]),
            Paragraph("<b>No. of PASS:</b> " + str(no_of_pass), style_right),
        ],
        [
            Paragraph(
                "<b>Siganture / Stamp:</b> _____________________________",
                styles["Normal"],
            ),
            Paragraph("<b>No. of FAIL: </b>" + str(no_of_fail), style_right),
        ],
    ]
    tbl = Table(tbl_data)
    Story.append(tbl)

    doc.build(Story)

    fs = FileSystemStorage(settings.MEDIA_ROOT + "/result_sheet")
    with fs.open(fname) as pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=" + fname + ""
        return response
    return response


@login_required
@student_required
def course_registration_form(request):
    current_session = Session.objects.get(is_current_session=True)
    courses = TakenCourse.objects.filter(student__student__id=request.user.id)
    fname = request.user.username + ".pdf"
    fname = fname.replace("/", "-")
    # flocation = '/tmp/' + fname
    # print(MEDIA_ROOT + "\\" + fname)
    flocation = settings.MEDIA_ROOT + "/registration_form/" + fname
    doc = SimpleDocTemplate(
        flocation, rightMargin=15, leftMargin=15, topMargin=0, bottomMargin=0
    )
    styles = getSampleStyleSheet()

    Story = [Spacer(1, 0.5)]
    Story.append(Spacer(1, 0.4 * inch))
    style = styles["Normal"]

    style = getSampleStyleSheet()
    normal = style["Normal"]
    normal.alignment = TA_CENTER
    normal.fontName = "Helvetica"
    normal.fontSize = 12
    normal.leading = 18
    title = "<b>EZOD UNIVERSITY OF TECHNOLOGY, ADAMA</b>"  # TODO: Make this dynamic
    title = Paragraph(title.upper(), normal)
    Story.append(title)
    style = getSampleStyleSheet()

    school = style["Normal"]
    school.alignment = TA_CENTER
    school.fontName = "Helvetica"
    school.fontSize = 10
    school.leading = 18
    school_title = (
        "<b>SCHOOL OF ELECTRICAL ENGINEERING & COMPUTING</b>"  # TODO: Make this dynamic
    )
    school_title = Paragraph(school_title.upper(), school)
    Story.append(school_title)

    style = getSampleStyleSheet()
    Story.append(Spacer(1, 0.1 * inch))
    department = style["Normal"]
    department.alignment = TA_CENTER
    department.fontName = "Helvetica"
    department.fontSize = 9
    department.leading = 18
    department_title = (
        "<b>DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING</b>"  # TODO: Make this dynamic
    )
    department_title = Paragraph(department_title, department)
    Story.append(department_title)
    Story.append(Spacer(1, 0.3 * inch))

    title = "<b><u>STUDENT COURSE REGISTRATION FORM</u></b>"
    title = Paragraph(title.upper(), normal)
    Story.append(title)
    student = Student.objects.get(student__pk=request.user.id)

    tbl_data = [
        [
            Paragraph(
                "<b>Registration Number : " + request.user.username.upper() + "</b>",
                styles["Normal"],
            )
        ],
        [
            Paragraph(
                "<b>Name : " + request.user.get_full_name.upper() + "</b>",
                styles["Normal"],
            )
        ],
        [
            Paragraph(
                "<b>Session : " + current_session.session.upper() + "</b>",
                styles["Normal"],
            ),
            Paragraph("<b>Level: " + student.level + "</b>", styles["Normal"]),
        ],
    ]
    tbl = Table(tbl_data)
    Story.append(tbl)
    Story.append(Spacer(1, 0.6 * inch))

    style = getSampleStyleSheet()
    semester = style["Normal"]
    semester.alignment = TA_LEFT
    semester.fontName = "Helvetica"
    semester.fontSize = 9
    semester.leading = 18
    semester_title = "<b>FIRST SEMESTER</b>"
    semester_title = Paragraph(semester_title, semester)
    Story.append(semester_title)

    # FIRST SEMESTER
    count = 0
    header = [
        (
            "S/No",
            "Course Code",
            "Course Title",
            "Unit",
            Paragraph("Name, Siganture of course lecturer & Date", style["Normal"]),
        )
    ]
    table_header = Table(header, 1 * [1.4 * inch], 1 * [0.5 * inch])
    table_header.setStyle(
        TableStyle(
            [
                ("ALIGN", (-2, -2), (-2, -2), "CENTER"),
                ("VALIGN", (-2, -2), (-2, -2), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ("VALIGN", (1, 0), (1, 0), "MIDDLE"),
                ("ALIGN", (0, 0), (0, 0), "CENTER"),
                ("VALIGN", (0, 0), (0, 0), "MIDDLE"),
                ("ALIGN", (-4, 0), (-4, 0), "LEFT"),
                ("VALIGN", (-4, 0), (-4, 0), "MIDDLE"),
                ("ALIGN", (-3, 0), (-3, 0), "LEFT"),
                ("VALIGN", (-3, 0), (-3, 0), "MIDDLE"),
                ("TEXTCOLOR", (0, -1), (-1, -1), colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
            ]
        )
    )
    Story.append(table_header)

    first_semester_unit = 0
    for course in courses:
        if course.course.semester == settings.FIRST:
            first_semester_unit += int(course.course.credit)
            data = [
                (
                    count + 1,
                    course.course.code.upper(),
                    Paragraph(course.course.title, style["Normal"]),
                    course.course.credit,
                    "",
                )
            ]
            count += 1
            table_body = Table(data, 1 * [1.4 * inch], 1 * [0.3 * inch])
            table_body.setStyle(
                TableStyle(
                    [
                        ("ALIGN", (-2, -2), (-2, -2), "CENTER"),
                        ("ALIGN", (1, 0), (1, 0), "CENTER"),
                        ("ALIGN", (0, 0), (0, 0), "CENTER"),
                        ("ALIGN", (-4, 0), (-4, 0), "LEFT"),
                        ("TEXTCOLOR", (0, -1), (-1, -1), colors.black),
                        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                        ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                    ]
                )
            )
            Story.append(table_body)

    style = getSampleStyleSheet()
    semester = style["Normal"]
    semester.alignment = TA_LEFT
    semester.fontName = "Helvetica"
    semester.fontSize = 8
    semester.leading = 18
    semester_title = (
        "<b>Total Second First Credit : " + str(first_semester_unit) + "</b>"
    )
    semester_title = Paragraph(semester_title, semester)
    Story.append(semester_title)

    # FIRST SEMESTER ENDS HERE
    Story.append(Spacer(1, 0.6 * inch))

    style = getSampleStyleSheet()
    semester = style["Normal"]
    semester.alignment = TA_LEFT
    semester.fontName = "Helvetica"
    semester.fontSize = 9
    semester.leading = 18
    semester_title = "<b>SECOND SEMESTER</b>"
    semester_title = Paragraph(semester_title, semester)
    Story.append(semester_title)
    # SECOND SEMESTER
    count = 0
    header = [
        (
            "S/No",
            "Course Code",
            "Course Title",
            "Unit",
            Paragraph(
                "<b>Name, Signature of course lecturer & Date</b>", style["Normal"]
            ),
        )
    ]
    table_header = Table(header, 1 * [1.4 * inch], 1 * [0.5 * inch])
    table_header.setStyle(
        TableStyle(
            [
                ("ALIGN", (-2, -2), (-2, -2), "CENTER"),
                ("VALIGN", (-2, -2), (-2, -2), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ("VALIGN", (1, 0), (1, 0), "MIDDLE"),
                ("ALIGN", (0, 0), (0, 0), "CENTER"),
                ("VALIGN", (0, 0), (0, 0), "MIDDLE"),
                ("ALIGN", (-4, 0), (-4, 0), "LEFT"),
                ("VALIGN", (-4, 0), (-4, 0), "MIDDLE"),
                ("ALIGN", (-3, 0), (-3, 0), "LEFT"),
                ("VALIGN", (-3, 0), (-3, 0), "MIDDLE"),
                ("TEXTCOLOR", (0, -1), (-1, -1), colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
            ]
        )
    )
    Story.append(table_header)

    second_semester_unit = 0
    for course in courses:
        if course.course.semester == settings.SECOND:
            second_semester_unit += int(course.course.credit)
            data = [
                (
                    count + 1,
                    course.course.code.upper(),
                    Paragraph(course.course.title, style["Normal"]),
                    course.course.credit,
                    "",
                )
            ]
            # color = colors.black
            count += 1
            table_body = Table(data, 1 * [1.4 * inch], 1 * [0.3 * inch])
            table_body.setStyle(
                TableStyle(
                    [
                        ("ALIGN", (-2, -2), (-2, -2), "CENTER"),
                        ("ALIGN", (1, 0), (1, 0), "CENTER"),
                        ("ALIGN", (0, 0), (0, 0), "CENTER"),
                        ("ALIGN", (-4, 0), (-4, 0), "LEFT"),
                        ("TEXTCOLOR", (0, -1), (-1, -1), colors.black),
                        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                        ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                    ]
                )
            )
            Story.append(table_body)

    style = getSampleStyleSheet()
    semester = style["Normal"]
    semester.alignment = TA_LEFT
    semester.fontName = "Helvetica"
    semester.fontSize = 8
    semester.leading = 18
    semester_title = (
        "<b>Total Second Semester Credit : " + str(second_semester_unit) + "</b>"
    )
    semester_title = Paragraph(semester_title, semester)
    Story.append(semester_title)

    Story.append(Spacer(1, 2))
    style = getSampleStyleSheet()
    certification = style["Normal"]
    certification.alignment = TA_JUSTIFY
    certification.fontName = "Helvetica"
    certification.fontSize = 8
    certification.leading = 18
    student = Student.objects.get(student__pk=request.user.id)
    certification_text = (
        "CERTIFICATION OF REGISTRATION: I certify that <b>"
        + str(request.user.get_full_name.upper())
        + "</b>\
    has been duly registered for the <b>"
        + student.level
        + " level </b> of study in the department\
    of COMPUTER SICENCE & ENGINEERING and that the courses and credits \
    registered are as approved by the senate of the University"
    )
    certification_text = Paragraph(certification_text, certification)
    Story.append(certification_text)

    # FIRST SEMESTER ENDS HERE

    logo = settings.STATICFILES_DIRS[0] + "/img/brand.png"
    im_logo = Image(logo, 1 * inch, 1 * inch)
    setattr(im_logo, "_offs_x", -218)
    setattr(im_logo, "_offs_y", 480)
    Story.append(im_logo)

    picture = settings.BASE_DIR + request.user.get_picture()
    im = Image(picture, 1.0 * inch, 1.0 * inch)
    setattr(im, "_offs_x", 218)
    setattr(im, "_offs_y", 550)
    Story.append(im)

    doc.build(Story)
    fs = FileSystemStorage(settings.MEDIA_ROOT + "/registration_form")
    with fs.open(fname) as pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=" + fname + ""
        return response
    return response

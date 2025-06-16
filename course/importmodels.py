# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse


class AccountsDepartmenthead(models.Model):
    id = models.BigAutoField(primary_key=True)
    department = models.ForeignKey('CourseProgram', models.DO_NOTHING, blank=True, null=True)
    user = models.OneToOneField('AccountsUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_departmenthead'


class AccountsParent(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=60, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    relation_ship = models.TextField()
    student = models.OneToOneField('AccountsStudent', models.DO_NOTHING, blank=True, null=True)
    user = models.OneToOneField('AccountsUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_parent'


class AccountsStudent(models.Model):
    id = models.BigAutoField(primary_key=True)
    level = models.CharField(max_length=25, blank=True, null=True)
    program = models.ForeignKey('CourseProgram', models.DO_NOTHING, blank=True, null=True)
    student = models.OneToOneField('AccountsUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_student'


class AccountsUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    is_student = models.IntegerField()
    is_lecturer = models.IntegerField()
    is_parent = models.IntegerField()
    is_dep_head = models.IntegerField()
    gender = models.CharField(max_length=1, blank=True, null=True)
    phone = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    picture = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    
    
    class Meta:
        managed = False
        db_table = 'accounts_user'


class AccountsUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_user_groups'
        unique_together = (('user', 'group'),)


class AccountsUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AutoNumbercount(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=90)  # Field name made lowercase.
    latest_number = models.CharField(max_length=90)
    last_updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auto_numbercount'


class Compensation(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    teacher_id = models.CharField(db_column='teacher_ID', max_length=90)  # Field name made lowercase.
    date = models.DateField()
    description = models.CharField(max_length=90)
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.
    seq = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'compensation'


class CoreActivitylog(models.Model):
    id = models.BigAutoField(primary_key=True)
    message = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'core_activitylog'


class CoreNewsandevents(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    posted_as = models.CharField(max_length=10)
    updated_date = models.DateTimeField(blank=True, null=True)
    upload_time = models.DateTimeField(blank=True, null=True)
    summary_en = models.TextField(blank=True, null=True)
    summary_ru = models.TextField(blank=True, null=True)
    title_en = models.CharField(max_length=200, blank=True, null=True)
    title_ru = models.CharField(max_length=200, blank=True, null=True)
    summary_es = models.TextField(blank=True, null=True)
    summary_fr = models.TextField(blank=True, null=True)
    title_es = models.CharField(max_length=200, blank=True, null=True)
    title_fr = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_newsandevents'


class CoreSemester(models.Model):
    id = models.BigAutoField(primary_key=True)
    semester = models.CharField(max_length=10)
    is_current_semester = models.IntegerField(blank=True, null=True)
    next_semester_begins = models.DateField(blank=True, null=True)
    session = models.ForeignKey('CoreSession', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_semester'


class CoreSession(models.Model):
    id = models.BigAutoField(primary_key=True)
    session = models.CharField(unique=True, max_length=200)
    is_current_session = models.IntegerField(blank=True, null=True)
    next_session_begins = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_session'


class CourseCourse(models.Model):
    id = models.BigAutoField(primary_key=True)
    slug = models.CharField(unique=True, max_length=50)
    title = models.CharField(max_length=200)
    code = models.CharField(unique=True, max_length=200)
    credit = models.IntegerField()
    summary = models.TextField()
    level = models.CharField(max_length=25)
    year = models.IntegerField()
    semester = models.CharField(max_length=200)
    is_elective = models.IntegerField()
    program = models.ForeignKey('CourseProgram', models.DO_NOTHING)
    summary_en = models.TextField(blank=True, null=True)
    summary_ru = models.TextField(blank=True, null=True)
    title_en = models.CharField(max_length=200, blank=True, null=True)
    title_ru = models.CharField(max_length=200, blank=True, null=True)
    summary_es = models.TextField(blank=True, null=True)
    summary_fr = models.TextField(blank=True, null=True)
    title_es = models.CharField(max_length=200, blank=True, null=True)
    title_fr = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_course'


class CourseCourseallocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    lecturer = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    session = models.ForeignKey(CoreSession, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_courseallocation'


class CourseCourseallocationCourses(models.Model):
    id = models.BigAutoField(primary_key=True)
    courseallocation = models.ForeignKey(CourseCourseallocation, models.DO_NOTHING)
    course = models.ForeignKey(CourseCourse, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'course_courseallocation_courses'
        unique_together = (('courseallocation', 'course'),)


class CourseCourseoffer(models.Model):
    id = models.BigAutoField(primary_key=True)
    dep_head = models.ForeignKey(AccountsDepartmenthead, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'course_courseoffer'


class CourseProgram(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=150)
    summary = models.TextField()
    summary_en = models.TextField(blank=True, null=True)
    summary_ru = models.TextField(blank=True, null=True)
    title_en = models.CharField(unique=True, max_length=150, blank=True, null=True)
    title_ru = models.CharField(unique=True, max_length=150, blank=True, null=True)
    summary_es = models.TextField(blank=True, null=True)
    summary_fr = models.TextField(blank=True, null=True)
    title_es = models.CharField(unique=True, max_length=150, blank=True, null=True)
    title_fr = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_program'


class CourseUpload(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    file = models.CharField(max_length=100)
    updated_date = models.DateTimeField()
    upload_time = models.DateTimeField()
    course = models.ForeignKey(CourseCourse, models.DO_NOTHING)
    title_en = models.CharField(max_length=100, blank=True, null=True)
    title_ru = models.CharField(max_length=100, blank=True, null=True)
    title_es = models.CharField(max_length=100, blank=True, null=True)
    title_fr = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_upload'


class CourseUploadvideo(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.CharField(unique=True, max_length=50)
    video = models.CharField(max_length=100)
    summary = models.TextField()
    timestamp = models.DateTimeField()
    course = models.ForeignKey(CourseCourse, models.DO_NOTHING)
    summary_en = models.TextField(blank=True, null=True)
    summary_ru = models.TextField(blank=True, null=True)
    title_en = models.CharField(max_length=100, blank=True, null=True)
    title_ru = models.CharField(max_length=100, blank=True, null=True)
    summary_es = models.TextField(blank=True, null=True)
    summary_fr = models.TextField(blank=True, null=True)
    title_es = models.CharField(max_length=100, blank=True, null=True)
    title_fr = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_uploadvideo'


class DashboardUserdashboardmodule(models.Model):
    title = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    app_label = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True)
    column = models.PositiveIntegerField()
    order = models.IntegerField()
    settings = models.TextField()
    children = models.TextField()
    collapsed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dashboard_userdashboardmodule'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Feegroup(models.Model):
    feegroupid = models.AutoField(db_column='FeeGroupID', primary_key=True)  # Field name made lowercase.
    feegroupname = models.CharField(db_column='FeeGroupName', max_length=100)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'feegroup'


class Grade(models.Model):
    stud = models.ForeignKey('Student', models.DO_NOTHING, db_column='Stud_ID')

    subject_code = models.ForeignKey('Subject', models.DO_NOTHING, db_column='subject_Code')
    stud_grade = models.CharField(db_column='stud_Grade', max_length=90)  # Field name made lowercase.
    academic_year = models.CharField(db_column='academic_Year', max_length=90)  # Field name made lowercase.
    grading_period = models.CharField(db_column='grading_Period', max_length=90)  # Field name made lowercase.
    gradelevel = models.CharField(db_column='GradeLevel', max_length=90)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'grade'
        unique_together = (('stud', 'subject_code', 'grading_period'),)


class Gradelevels(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    grade_level = models.CharField(db_column='grade_Level', max_length=90)  # Field name made lowercase.
    adviser = models.CharField(max_length=90)
    school_year = models.CharField(db_column='school_Year', max_length=90)  # Field name made lowercase.
    semester = models.CharField(db_column='Semester', max_length=90)  # Field name made lowercase.
    strand = models.CharField(db_column='Strand', max_length=90)  # Field name made lowercase.
    section = models.CharField(max_length=90)

    class Meta:
        managed = False
        db_table = 'gradelevels'
    
    def get_absolute_url(self):
        return reverse("program_detail", kwargs={"pk": self.ref})
    

class Benefits(models.Model):
    ref = models.AutoField(primary_key=True)
    stud = models.ForeignKey('Student', on_delete=models.CASCADE, db_column='Stud_ID')
    type = models.CharField(max_length=90, null=True, blank=True)
    description = models.CharField(max_length=90, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    school_year = models.CharField(max_length=90, null=True, blank=True)
    jour_code = models.IntegerField(null=True, blank=True)
    referenceno = models.CharField(max_length=90)

    class Meta:
        db_table = 'benefits'

    def __str__(self):
        return f"{self.stud} - {self.description} - {self.amount}"


class Guardian(models.Model):
    gid = models.AutoField(db_column='GID', primary_key=True)  # Field name made lowercase.
    stud_id = models.CharField(db_column='Stud_ID', max_length=90)  # Field name made lowercase.
    last_name = models.CharField(db_column='last_Name', max_length=90)  # Field name made lowercase.
    first_name = models.CharField(db_column='first_Name', max_length=90)  # Field name made lowercase.
    middle_name = models.CharField(db_column='middle_Name', max_length=90)  # Field name made lowercase.
    relationship = models.CharField(max_length=90)
    occupation = models.CharField(max_length=90)
    noe = models.CharField(db_column='NOE', max_length=90)  # Field name made lowercase.
    business = models.CharField(max_length=90)
    email_address = models.CharField(db_column='email_Address', max_length=90)  # Field name made lowercase.
    contact_no = models.CharField(db_column='contact_No', max_length=90)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=90)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'guardian'


class JetBookmark(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True)
    date_add = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'jet_bookmark'


class JetPinnedapplication(models.Model):
    app_label = models.CharField(max_length=255)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True)
    date_add = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'jet_pinnedapplication'


class JournalCode(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=90)  # Field name made lowercase.
    latest_number = models.CharField(max_length=90)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'journal_code'


class Monitoring(models.Model):
    mon_id = models.AutoField(db_column='mon_ID', primary_key=True)  # Field name made lowercase.
    teacher_id = models.CharField(db_column='teacher_ID', max_length=90)  # Field name made lowercase.
    date = models.DateField()
    comment = models.CharField(max_length=90)
    academic_year = models.CharField(db_column='academic_Year', max_length=90)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'monitoring'


class OpenAccount(models.Model):
    account_id = models.IntegerField(db_column='Account_ID')  # Field name made lowercase.
    account_type = models.IntegerField(db_column='Account_Type')  # Field name made lowercase.
    account_name = models.IntegerField(db_column='Account_Name')  # Field name made lowercase.
    contact_info = models.IntegerField(db_column='Contact_Info')  # Field name made lowercase.
    balance = models.IntegerField(db_column='Balance')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'open_account'


class Parent(models.Model):
    pid = models.AutoField(db_column='PID', primary_key=True)  # Field name made lowercase.
    last_name = models.CharField(db_column='last_Name', max_length=90)  # Field name made lowercase.
    first_name = models.CharField(db_column='first_Name', max_length=90)  # Field name made lowercase.
    middle_name = models.CharField(db_column='middle_Name', max_length=90)  # Field name made lowercase.
    occupation = models.CharField(max_length=90)
    noe = models.CharField(db_column='NOE', max_length=90)  # Field name made lowercase.
    business = models.CharField(max_length=90)
    email_address = models.CharField(db_column='email_Address', max_length=90)  # Field name made lowercase.
    contact_no = models.CharField(db_column='contact_No', max_length=11)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=90)  # Field name made lowercase.
    income = models.IntegerField(db_column='Income')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'parent'


class Parentstudent(models.Model):
    gid = models.IntegerField(db_column='GID', primary_key=True)  # Field name made lowercase.
    stud_id = models.CharField(db_column='Stud_ID', max_length=90)  # Field name made lowercase.
    relationship = models.CharField(max_length=90)
    isguardian = models.IntegerField(db_column='isGuardian')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'parentstudent'
        unique_together = (('gid', 'stud_id'),)


class PaymentsInvoice(models.Model):
    id = models.BigAutoField(primary_key=True)
    total = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    payment_complete = models.IntegerField()
    invoice_code = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'payments_invoice'


class PrDetails(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    pr_id = models.CharField(db_column='pr_ID', max_length=90)  # Field name made lowercase.
    description = models.CharField(max_length=90)
    des_value = models.CharField(max_length=90)
    seq = models.IntegerField()
    teacher_id = models.CharField(db_column='teacher_ID', max_length=90)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pr_details'


class Preliminarycharges(models.Model):
    pc_id = models.AutoField(db_column='PC_ID', primary_key=True)  # Field name made lowercase.
    grade_level = models.CharField(db_column='grade_Level', max_length=90)  # Field name made lowercase.
    name = models.CharField(max_length=90)
    description = models.CharField(max_length=90)
    academic_year = models.CharField(db_column='academic_Year', max_length=90)  # Field name made lowercase.
    date_added = models.DateField(db_column='date_Added')  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount')  # Field name made lowercase.
    jour_code = models.IntegerField()
    feegroupid = models.IntegerField(db_column='FeeGroupID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'preliminarycharges'


class Previousschooling(models.Model):
    ps_id = models.AutoField(db_column='ps_ID', primary_key=True)  # Field name made lowercase.
    stud_id = models.CharField(db_column='Stud_ID', max_length=90)  # Field name made lowercase.
    grade_level = models.CharField(db_column='grade_Level', max_length=90)  # Field name made lowercase.
    nosa = models.CharField(db_column='NOSA', max_length=90)  # Field name made lowercase.
    address = models.CharField(max_length=90)
    year_attended = models.CharField(db_column='year_Attended', max_length=90)  # Field name made lowercase.
    reasonfortransfer = models.CharField(db_column='ReasonForTransfer', max_length=90)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'previousschooling'


class QuizChoice(models.Model):
    id = models.BigAutoField(primary_key=True)
    choice_text = models.CharField(max_length=1000)
    correct = models.IntegerField()
    question = models.ForeignKey('QuizMcquestion', models.DO_NOTHING)
    choice_text_en = models.CharField(max_length=1000, blank=True, null=True)
    choice_text_ru = models.CharField(max_length=1000, blank=True, null=True)
    choice_text_es = models.CharField(max_length=1000, blank=True, null=True)
    choice_text_fr = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quiz_choice'


class QuizEssayquestion(models.Model):
    question_ptr = models.OneToOneField('QuizQuestion', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'quiz_essayquestion'


class QuizMcquestion(models.Model):
    question_ptr = models.OneToOneField('QuizQuestion', models.DO_NOTHING, primary_key=True)
    choice_order = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'quiz_mcquestion'


class QuizProgress(models.Model):
    id = models.BigAutoField(primary_key=True)
    score = models.CharField(max_length=1024)
    user = models.OneToOneField(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'quiz_progress'


class QuizQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    figure = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    explanation = models.TextField()
    content_en = models.CharField(max_length=1000, blank=True, null=True)
    content_ru = models.CharField(max_length=1000, blank=True, null=True)
    explanation_en = models.TextField(blank=True, null=True)
    explanation_ru = models.TextField(blank=True, null=True)
    content_es = models.CharField(max_length=1000, blank=True, null=True)
    content_fr = models.CharField(max_length=1000, blank=True, null=True)
    explanation_es = models.TextField(blank=True, null=True)
    explanation_fr = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quiz_question'


class QuizQuestionQuiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(QuizQuestion, models.DO_NOTHING)
    quiz = models.ForeignKey('QuizQuiz', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'quiz_question_quiz'
        unique_together = (('question', 'quiz'),)


class QuizQuiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=60)
    slug = models.CharField(unique=True, max_length=50)
    description = models.TextField()
    category = models.CharField(max_length=20)
    random_order = models.IntegerField()
    answers_at_end = models.IntegerField()
    exam_paper = models.IntegerField()
    single_attempt = models.IntegerField()
    pass_mark = models.SmallIntegerField()
    draft = models.IntegerField()
    timestamp = models.DateTimeField()
    course = models.ForeignKey(CourseCourse, models.DO_NOTHING)
    description_en = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    title_en = models.CharField(max_length=60, blank=True, null=True)
    title_ru = models.CharField(max_length=60, blank=True, null=True)
    description_es = models.TextField(blank=True, null=True)
    description_fr = models.TextField(blank=True, null=True)
    title_es = models.CharField(max_length=60, blank=True, null=True)
    title_fr = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quiz_quiz'


class QuizSitting(models.Model):
    id = models.BigAutoField(primary_key=True)
    question_order = models.CharField(max_length=1024)
    question_list = models.CharField(max_length=1024)
    incorrect_questions = models.CharField(max_length=1024)
    current_score = models.IntegerField()
    complete = models.IntegerField()
    user_answers = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    course = models.ForeignKey(CourseCourse, models.DO_NOTHING)
    quiz = models.ForeignKey(QuizQuiz, models.DO_NOTHING)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'quiz_sitting'


class Requirements(models.Model):
    req_id = models.IntegerField(db_column='req_ID', primary_key=True)  # Field name made lowercase.
    r_name = models.CharField(db_column='r_Name', max_length=90)  # Field name made lowercase.
    isactive = models.IntegerField(db_column='isActive')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'requirements'


class Requirementsbridge(models.Model):
    req_id = models.IntegerField(db_column='req_ID', primary_key=True)  # Field name made lowercase.
    stud_id = models.CharField(db_column='Stud_ID', max_length=90)  # Field name made lowercase.
    datepass = models.DateField(db_column='datePass')  # Field name made lowercase.
    note = models.CharField(max_length=90)
    ispass = models.IntegerField(db_column='isPass')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'requirementsbridge'
        unique_together = (('req_id', 'stud_id'),)


class ResultResult(models.Model):
    id = models.BigAutoField(primary_key=True)
    gpa = models.FloatField(blank=True, null=True)
    cgpa = models.FloatField(blank=True, null=True)
    semester = models.CharField(max_length=100)
    session = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=25, blank=True, null=True)
    student = models.ForeignKey(AccountsStudent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'result_result'


class ResultTakencourse(models.Model):
    id = models.BigAutoField(primary_key=True)
    assignment = models.DecimalField(max_digits=5, decimal_places=2)
    mid_exam = models.DecimalField(max_digits=5, decimal_places=2)
    quiz = models.DecimalField(max_digits=5, decimal_places=2)
    attendance = models.DecimalField(max_digits=5, decimal_places=2)
    final_exam = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)
    point = models.DecimalField(max_digits=5, decimal_places=2)
    comment = models.CharField(max_length=200)
    course = models.ForeignKey(CourseCourse, models.DO_NOTHING)
    student = models.ForeignKey(AccountsStudent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'result_takencourse'


class Scharges(models.Model):
    table_pk = models.AutoField(db_column='table_PK', primary_key=True)  # Field name made lowercase.
    stud_id = models.CharField(db_column='Stud_ID', max_length=90)  # Field name made lowercase.
    date = models.DateField()
    name = models.CharField(db_column='Name', max_length=90)  # Field name made lowercase.
    description = models.CharField(max_length=90)
    amount = models.IntegerField(db_column='Amount')  # Field name made lowercase.
    atm_balance = models.IntegerField(db_column='ATM_Balance')  # Field name made lowercase.
    jour_code = models.IntegerField()
    referenceno = models.CharField(max_length=90, blank=True, null=True)
    accountname = models.CharField(db_column='AccountName', max_length=90)  # Field name made lowercase.
    feegroup = models.CharField(db_column='FeeGroup', max_length=90, blank=True, null=True)  # Field name made lowercase.
    school_year = models.CharField(db_column='School_Year', max_length=90)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'scharges'


class Spayment(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    table_pk = models.CharField(db_column='table_PK', max_length=90)  # Field name made lowercase.
    stud_id = models.CharField(db_column='Stud_ID', max_length=90)  # Field name made lowercase.
    date = models.DateField()
    description = models.CharField(max_length=90)
    amount = models.IntegerField(db_column='Amount')  # Field name made lowercase.
    atm_balance = models.IntegerField(db_column='ATM_Balance')  # Field name made lowercase.
    jour_code = models.IntegerField()
    referenceno = models.CharField(max_length=90, blank=True, null=True)
    accountname = models.CharField(db_column='AccountName', max_length=90, blank=True, null=True)  # Field name made lowercase.
    school_year = models.CharField(db_column='School_Year', max_length=90)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=90)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'spayment'


class StaffPosition(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    empid = models.CharField(db_column='empID', max_length=90)  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=90)  # Field name made lowercase.
    salary = models.FloatField(db_column='Salary')  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    date_until = models.DateField()

    class Meta:
        managed = False
        db_table = 'staff_position'


class Standardfinancialdescription(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    financial_description = models.CharField(db_column='financial_Description', max_length=90)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'standardfinancialdescription'


class Standardgradelevel(models.Model):
    grade_level_name = models.CharField(db_column='grade_Level_Name', primary_key=True, max_length=90)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'standardgradelevel'


class Standardschoolyear(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    school_year_name = models.CharField(db_column='school_Year_Name', max_length=90)  # Field name made lowercase.
    isactive = models.IntegerField(db_column='isActive')  # Field name made lowercase.
    starting_date = models.DateField(db_column='Starting_Date')  # Field name made lowercase.
    ending_date = models.DateField(db_column='Ending_Date')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'standardschoolyear'


class Standardsubjecttime(models.Model):
    subject_time_name = models.CharField(db_column='subject_Time_Name', primary_key=True, max_length=90)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'standardsubjecttime'


class Attendance(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)  # Field name made lowercase.
    date = models.DateField(db_column='date',)
    cl = models.CharField(db_column='cl',max_length=10)
    present_status = models.CharField(db_column='present_status',max_length=10)
    stud = models.CharField(db_column='stud',max_length=10, blank=True, null=True)
    subject_code = models.CharField(db_column='subject_code', max_length=90)

    class Meta:
        managed = False
        db_table = 'school_attendance'



class Student(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    studentid = models.CharField(db_column='StudentID', max_length=90)  # Field name made lowercase.
    lrn_no = models.CharField(db_column='LRN_No', max_length=90)  # Field name made lowercase.
    last_name = models.CharField(db_column='last_Name', max_length=90)  # Field name made lowercase.
    first_name = models.CharField(db_column='first_Name', max_length=90)  # Field name made lowercase.
    middle_name = models.CharField(db_column='middle_Name', max_length=90)  # Field name made lowercase.
    nick_name = models.CharField(db_column='nick_Name', max_length=90)  # Field name made lowercase.
    sex = models.CharField(max_length=90)
    dob = models.DateField(db_column='DOB')  # Field name made lowercase.
    age = models.CharField(max_length=90)
    bo = models.CharField(db_column='BO', max_length=1000)  # Field name made lowercase.
    home_address = models.CharField(db_column='home_Address', max_length=90)  # Field name made lowercase.
    religion = models.CharField(max_length=90)
    tvprogramsmoviesbooks = models.CharField(db_column='TVProgramsMoviesBooks', max_length=90)  # Field name made lowercase.
    first_language = models.CharField(db_column='first_Language', max_length=90)  # Field name made lowercase.
    language_spoken = models.CharField(db_column='language_Spoken', max_length=90, blank=True, null=True)  # Field name made lowercase.
    pob = models.CharField(db_column='POB', max_length=90, blank=True, null=True)  # Field name made lowercase.
    interest = models.CharField(db_column='Interest', max_length=90, blank=True, null=True)  # Field name made lowercase.
    if_voucher = models.IntegerField(db_column='If_Voucher', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=90)
    rfid = models.CharField(max_length=90, blank=True, null=True)


    @property
    def get_full_name(self):
        full_name = self.first_name
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name


    def __str__(self):
        return f"{self.first_name} {self.last_name}" 
    
        
    class Meta:
        managed = False
        db_table = 'student'


class Studentenrollsubject(models.Model):
    sr = models.ForeignKey('Studentregister', db_column='SR_ID', to_field='sr_id', on_delete=models.DO_NOTHING)
    subject = models.ForeignKey('Subject', db_column='subject_Code', to_field='ref', on_delete=models.DO_NOTHING)
    ref = models.AutoField(db_column='Ref', primary_key=True)

    class Meta:
        managed = False
        db_table = 'studentenrollsubject'
    
    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"ref": self.subject.ref})  


class Studentregister(models.Model):
    sr_id = models.CharField(db_column='SR_ID', primary_key=True, max_length=90)  # Field name made lowercase.
    stud_id = models.CharField(db_column='Stud_ID', max_length=90)  # Field name made lowercase.
    academic_year = models.CharField(db_column='academic_Year', max_length=90)  # Field name made lowercase.
    grade_level = models.CharField(db_column='grade_Level', max_length=90)  # Field name made lowercase.
    dor = models.DateField(db_column='DOR')  # Field name made lowercase.
    nos = models.CharField(db_column='NOS', max_length=90)  # Field name made lowercase.
    nosar = models.CharField(db_column='NOSAR', max_length=90)  # Field name made lowercase.
    strand = models.CharField(db_column='Strand', max_length=90)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=90)  # Field name made lowercase.
    date_entered = models.DateField(blank=True, null=True)
    resident = models.CharField(db_column='Resident', max_length=90)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'studentregister'
    


class Subject(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    subject_code = models.CharField(db_column='subject_Code', max_length=90)  # Field name made lowercase.
    sub_name = models.CharField(db_column='sub_Name', max_length=90)  # Field name made lowercase.
    sub_time = models.CharField(db_column='sub_Time', max_length=90)  # Field name made lowercase.
    sub_room = models.CharField(db_column='sub_Room', max_length=90)  # Field name made lowercase.
    teacher_id = models.CharField(db_column='teacher_ID', max_length=90)  # Field name made lowercase.
    grade_level = models.IntegerField(db_column='grade_Level')  # Field name made lowercase.
    academic_year = models.CharField(db_column='academic_Year', max_length=90)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'subject'
        
    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"ref": self.ref})    


class Systemaccount(models.Model):
    sa_no = models.AutoField(db_column='SA_No', primary_key=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', max_length=90)  # Field name made lowercase.
    name = models.CharField(max_length=90)
    email_address = models.CharField(db_column='email_Address', max_length=90)  # Field name made lowercase.
    password = models.CharField(max_length=90)
    username = models.CharField(max_length=90)
    contact_no = models.CharField(db_column='contact_No', max_length=90)  # Field name made lowercase.
    position = models.CharField(max_length=90)
    picture = models.TextField(db_column='Picture')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'systemaccount'
        unique_together = (('sa_no', 'id', 'username'),)


class Tcharges(models.Model):
    tc_id = models.AutoField(db_column='tc_ID', primary_key=True)  # Field name made lowercase.
    teacher_id = models.CharField(db_column='teacher_ID', max_length=90)  # Field name made lowercase.
    date = models.CharField(max_length=90)
    description = models.CharField(max_length=90)
    amount = models.IntegerField(db_column='Amount')  # Field name made lowercase.
    atm_balance = models.CharField(db_column='ATM_Balance', max_length=90)  # Field name made lowercase.
    seq = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tcharges'


class Teacher(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    teacher_id = models.CharField(db_column='teacher_ID', max_length=90)  # Field name made lowercase.
    last_name = models.CharField(db_column='last_Name', max_length=90)  # Field name made lowercase.
    first_name = models.CharField(db_column='first_Name', max_length=90)  # Field name made lowercase.
    middle_name = models.CharField(db_column='middle_Name', max_length=90)  # Field name made lowercase.
    sex = models.CharField(max_length=90)
    status = models.CharField(max_length=90)
    dob = models.DateField(db_column='DOB')  # Field name made lowercase.
    age = models.IntegerField()
    home_address = models.CharField(db_column='home_Address', max_length=90)  # Field name made lowercase.
    contact_no = models.IntegerField(db_column='contact_No')  # Field name made lowercase.
    salary = models.FloatField(db_column='Salary')  # Field name made lowercase.


    def __str__(self):
        return f"{self.first_name} {self.last_name}" 

    class Meta:
        managed = False
        db_table = 'teacher'


class TeacherPayroll(models.Model):
    ref = models.AutoField(db_column='Ref', primary_key=True)  # Field name made lowercase.
    trans_id = models.CharField(db_column='Trans_ID', max_length=90)  # Field name made lowercase.
    emp_id = models.CharField(db_column='emp_ID', max_length=90)  # Field name made lowercase.
    pr_month = models.CharField(max_length=90)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'teacher_payroll'


class TeacherTeacher(models.Model):
    profile_pic = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20)
    status = models.IntegerField()
    user_id = models.IntegerField(unique=True)
    salary = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teacher_teacher'


class UploadedFiles(models.Model):
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_type = models.CharField(max_length=50, blank=True, null=True)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    uploaded_at = models.DateTimeField()
    file_owner = models.CharField(max_length=90)

    class Meta:
        managed = False
        db_table = 'uploaded_files'



class License(models.Model):
    lisense = models.CharField(max_length=90, unique=True)  # matches varchar(90)
    dateended = models.DateField()  # or DateTimeField() if you want time as well

    class Meta:
        managed = False
        db_table = 'aimsvalidation'
from django.urls import path
from . import views


urlpatterns = [
    # Program urls
    path("", views.ProgramFilterView.as_view(), name="programs"),
    path("<int:pk>/detail/", views.program_detail, name="program_detail"),
    path("add/", views.program_add, name="add_program"),
    path("<int:pk>/edit/", views.program_edit, name="edit_program"),
    path("<int:pk>/delete/", views.program_delete, name="program_delete"),
    # Course urls
    path("course/<ref>/detail/", views.course_single, name="course_detail"),
    path("<int:pk>/course/add/", views.course_add, name="course_add"),
    path("course/<slug>/edit/", views.course_edit, name="edit_course"),
    path("course/delete/<slug>/", views.course_delete, name="delete_course"),
    
      
    path('attendance/save/<int:course_id>/', views.save_attendance, name='save_attendance'),
    
    # path("attendance/view/<slug>/", views.course_delete, name="delete_course"),
        
    path('student-soa/', views.student_soa, name='student-soa'),
    
    path('attendance/pdf/<str:course_id>/', views.attendance_pdf, name='attendance_pdf'),

    
    
     path('attendance/<int:course_id>/', views.view_attendance, name='view_attendance'),  # <- new line
    # CourseAllocation urls
    path(
        "course/assign/",
        views.CourseAllocationFormView.as_view(),
        name="course_allocation",
    ),
    path(
        "course/allocated/",
        views.CourseAllocationFilterView.as_view(),
        name="course_allocation_view",
    ),
    path(
        "allocated_course/<int:pk>/edit/",
        views.edit_allocated_course,
        name="edit_allocated_course",
    ),
    path(
        "course/<int:pk>/deallocate/", views.deallocate_course, name="course_deallocate"
    ),
    # File uploads urls
    path(
        "course/<ref>/documentations/upload/",
        views.handle_file_upload,
        name="upload_file_view",
    ),
    path(
        "course/<slug>/documentations/<int:file_id>/edit/",
        views.handle_file_edit,
        name="upload_file_edit",
    ),
    path(
        "course/<slug>/documentations/<int:file_id>/delete/",
        views.handle_file_delete,
        name="upload_file_delete",
    ),
    # Video uploads urls
    path(
        "course/<ref>/video_tutorials/upload/",
        views.handle_video_upload,
        name="upload_video",
    ),
    path(
        "course/<ref>/video_tutorials/<video_slug>/detail/",
        views.handle_video_single,
        name="video_single",
    ),
    path(
        "course/<ref>/video_tutorials/<video_slug>/edit/",
        views.handle_video_edit,
        name="upload_video_edit",
    ),
    path(
        "course/<ref>/video_tutorials/<video_slug>/delete/",
        views.handle_video_delete,
        name="upload_video_delete",
    ),
    # course registration
    path("course/registration/", views.course_registration, name="course_registration"),
    path("course/drop/", views.course_drop, name="course_drop"),
    path("my_courses/", views.user_course_list, name="user_course_list"),    
    
    path('programs/grade/<int:course_id>/', views.view_grade, name='view_grade'),
    # In urls.py
    path('grade/delete/<int:student_id>/<int:course_id>/<str:period>/', views.delete_grade, name='delete_grade'),

]


from django.urls import path
from school_system_app import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('play_video/', views.play_video, name='play_video'),

    path('login/',views.LoginView, name='user_login'),
    path('logout/',views.logoutView, name='user_logout'),

    path('register/',views.Register, name='register'),

    path('student-register/', views.StudentRegister, name='student_registration'),
    path('teacher-register/', views.TeacherRegister, name='teacher_registration'),

    path('assignment-creation/', views.CreateAssignment, name="assignment_creation"),
    path('assignment-submission/', views.SubmitAssignment, name="assignment_submission"),

    path('view-assignments/',views.ViewAssignments, name='view_assignments'),
    path('update-assignment/<int:id>/', views.UpdateAssignment, name='update_assignment'),

    path('list-submissions/', views.ViewSubmittedAssignments, name="list_submissions"),
    path('view-submits/', views.ViewSubmissions, name="view_submits"),

    path('student-file-retrieve/<int:submission_id>/', views.StudentFileRetrieve, name="student_file_retrieve"),
    path('teacher-file-retrieve/<int:submission_id>/', views.TeacherFileRetrieve, name="teacher_file_retrieve"),
    path('update-score/<int:submission_id>/', views.ScoreUpdate, name='score_update'),

    path('my-profile/', views.ProfileView, name="my_profile"),
    path('my-profile/<int:id>/update/', views.admin_update, name='admin_update'),

    path('admin-page/', views.AdminPage, name = "admin_page"),

    path('students/', views.student_list, name='student_list'),
    path('students/<int:id>/update/', views.student_update, name='student_update'),
    path('students/<int:id>/deactivate/', views.student_deactivate, name='student_deactivate'),
    path('students/<int:id>/activate/', views.student_activate, name='student_activate'),
 
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:id>/update/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:id>/deactivate/', views.teacher_deactivate, name='teacher_deactivate'),
    path('teachers/<int:id>/activate/', views.teacher_activate, name='teacher_activate'),

    path('permission-denied/', views.PermissionDenied, name='permission_denied'),

    path('reset-password/', auth_views.PasswordResetView.as_view(
        template_name='passwords/password_reset_form.html'), name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='passwords/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='passwords/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='passwords/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
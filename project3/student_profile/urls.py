from django.urls import path
from project3.student_profile import views

urlpatterns = [
    path('register/', views.StudentRegisterView.as_view(), name='student-register'),
    path('login/', views.StudentUserLoginView.as_view(), name='student-login'),
    path('dashboard/', views.student_dashboard, name='student-dashboard'),
    path('logout/', views.StudentLogoutView.as_view(), name='student-logout-register'),
    path('student-personal-dashboard/', views.student_personal_dashboard, name='student-personal-dashboard'),
    path('apply/<int:course_id>/', views.apply_to_course, name='apply-to-course'),
    path('my-courses/', views.my_courses, name='student-personal-dashboard'),
    path('course/<int:course_id>/', views.student_course_details, name='course-details'),
    path('remove/<int:course_id>/', views.remove_course, name='remove-course'),
    path('course/<int:pk>/upload-homework/', views.upload_homework, name='upload-homework'),
    path('course/<int:pk>/delete-homework/', views.delete_homework, name='delete-homework'),

    path('edit/', views.StudentEditView.as_view(), name='student-profile-edit-page'),
    path('delete/', views.StudentDeleteView.as_view(), name='student-profile-delete-page'),
]
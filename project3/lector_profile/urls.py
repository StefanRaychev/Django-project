from django.urls import path
from project3.lector_profile import views

'''
path('create/', views.lecture_profile_create, name='lector-create-profile'),
path('edit/', views.edit_lector_profile, name='lector-edit-profile'),
path('delete/', views.delete_lector_profile, name='lector-delete-profile'),
path('delete/confirm/', views.lector_delete_profile_confirm, name='lector-delete-profile-confirm'),
'''


urlpatterns = [
    path('register/', views.LectorRegisterView.as_view(), name='lector-register'),
    path('login/', views.LectorLoginView.as_view(), name='lector-login'),
    path('dashboard/', views.lector_dashboard, name='lector_dashboard'),
    path('logout/', views.LectorLogoutView.as_view(), name='lector-logout'),
    path('edit/', views.LectorEditView.as_view(), name='lector-profile-edit'),
    path('delete/', views.LectorDeleteView.as_view(), name='lector-profile-delete'),
    path('my-dashboard/', views.lector_personal_dashboard, name='lector_personal_dashboard'),
    path('create-course/', views.CreateCourseView.as_view(), name='create-course-page'),
    path('edit-course/<int:pk>/', views.EditCourseView.as_view(), name='lector-course-edit'),
    path('delete-course/<int:pk>/', views.CourseDeleteView.as_view(), name='delete-course'),
    path('course/<int:pk>/', views.LectorCourseDetailView.as_view(), name='lector-course-detail'),
    path('course/<int:pk>/upload-textbook/', views.upload_textbook, name='upload-textbook'),
    path('course/<int:pk>/delete-textbook/', views.delete_textbook, name='delete-textbook'),
    path('all-dashboard/', views.all_dashboard, name='lector_dashboard'),
    path('lector/course/<int:course_id>/student/<int:student_id>/', views.view_student_homework, name='view-student-homework'),
    path('course/<int:pk>/student/<int:student_pk>/update-score/', views.update_student_score, name='update-student-score'),

]

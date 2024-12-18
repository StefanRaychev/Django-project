from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic.edit import DeleteView
from project3.accounts.models import CustomUser
from project3.lector_profile.models import NewCourse, Homework, StudentCourse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import StudentRegistrationForm, StudentLoginForm, StudentProfileEditForm


class StudentRegisterView(CreateView):
    model = CustomUser
    form_class = StudentRegistrationForm
    template_name = 'student-registration.html'
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Log the user in after registration
        return response


class StudentUserLoginView(auth_views.LoginView):
    form_class = StudentLoginForm
    template_name = 'student_dashboard.html'
    next_page = reverse_lazy('student-dashboard')


def student_dashboard(request):
    courses = NewCourse.objects.all()  # Fetch all courses

    return render(request, 'student_dashboard.html', {'courses': courses})


def student_personal_dashboard(request):
    # Fetch all courses created by the logged-in user
    courses = NewCourse.objects.filter(author=request.user)
    return render(request, 'student_personal_dashboard.html', {'courses': courses})


class StudentLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('student-login-register')


class StudentEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser  # Use CustomUser as defined in AUTH_USER_MODEL
    form_class = StudentProfileEditForm
    template_name = 'student-profile-edit-page.html'

    def get_object(self, queryset=None):
        # Fetch the profile of the logged-in user
        return get_object_or_404(CustomUser, pk=self.request.user.pk)

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user back in after the profile is updated
        user = form.instance
        login(self.request, user)
        return response

    def get_success_url(self):
        # Redirect to the dashboard after saving changes
        return reverse_lazy('student-dashboard')


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'student-profile-delete-confirmation.html'

    def get_object(self, queryset=None):
        # Fetch the profile of the logged-in user
        return get_object_or_404(CustomUser, pk=self.request.user.pk)

    def get_success_url(self):
        # Redirect to the home page after deletion
        return reverse_lazy('home-page')


@login_required
def apply_to_course(request, course_id):
    # Fetch the course the student wants to apply for
    course = get_object_or_404(NewCourse, id=course_id)

    # Add the student to the course's students field
    course.students.add(request.user)

    # Redirect back to the all courses page
    return redirect('student-dashboard')


def my_courses(request):
    # Fetch courses where the logged-in user has applied
    courses = NewCourse.objects.filter(students=request.user)
    return render(request, 'student_personal_dashboard.html', {'courses': courses})


def student_course_details(request, course_id):
    # Get the course by its ID
    course = get_object_or_404(NewCourse, id=course_id)
    student = request.user  # Assuming the logged-in user is the student

    # Fetch the StudentCourse relationship
    student_course = StudentCourse.objects.filter(course=course, student=student).first()
    score = student_course.score if student_course else None

    print(f"Textbooks for course {course.title}: {course.textbooks}")  # Debugging print
    print(f"Score for student {student.username} in course {course.title}: {score}")  # Debugging print

    # Pass both the course and the score to the template
    return render(request, 'course_details.html', {'course': course, 'score': score})



def remove_course(request, course_id):
    # Get the course by its ID
    course = get_object_or_404(NewCourse, id=course_id)

    # Remove the logged-in student from the course's students
    course.students.remove(request.user)

    # Redirect to the student's "My Dashboard"
    return redirect('student-personal-dashboard')


@csrf_exempt
def upload_homework(request, pk):
    course = get_object_or_404(NewCourse, pk=pk)
    if request.method == 'POST' and request.FILES.getlist('homeworks'):
        student_id = request.POST.get('student_id')  # Get the student ID from the form
        student = get_object_or_404(CustomUser, pk=student_id)  # Fetch the student instance
        for file in request.FILES.getlist('homeworks'):
            Homework.objects.create(
                course=course,
                student=student,  # Use the fetched student
                file=file,
                uploaded_by=request.user  # Track the uploader
            )
    return redirect('course-details', course_id=pk)


@csrf_exempt
def delete_homework(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    if request.method == 'POST':
        homework.file.delete()
        homework.delete()
    return redirect('course-details', course_id=homework.course.pk)
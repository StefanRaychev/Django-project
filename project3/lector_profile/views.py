from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic.edit import DeleteView
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from project3.accounts.models import CustomUser
from decimal import Decimal, InvalidOperation

from .forms import LectorRegistrationForm, LoginForm, ProfileEditForm, CourseCreationForm
from .models import NewCourse, Textbook, Homework, StudentCourse


class LectorRegisterView(CreateView):
    model = CustomUser
    form_class = LectorRegistrationForm
    template_name = 'lector_registration.html'
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Log the user in after registration
        return response


class LectorLoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'lector_login_page.html'
    next_page = reverse_lazy('lector_dashboard')


def lector_dashboard(request):
    lectors = CustomUser.objects.filter(role='lector')
    return render(request, 'lector_dashboard.html', {'lectors': lectors})


def lector_personal_dashboard(request):
    # Fetch all courses created by the logged-in user
    courses = NewCourse.objects.filter(author=request.user)
    return render(request, 'lector_personal_dashboard.html', {'courses': courses})


class LectorLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('lector-register')


class LectorEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser  # Use CustomUser as defined in AUTH_USER_MODEL
    form_class = ProfileEditForm
    template_name = 'lector_profile_edit.html'

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
        return reverse_lazy('lector_dashboard')


class LectorDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'lector_profile_delete_confirmation.html'

    def get_object(self, queryset=None):
        # Fetch the profile of the logged-in user
        return get_object_or_404(CustomUser, pk=self.request.user.pk)

    def get_success_url(self):
        # Redirect to the home page after deletion
        return reverse_lazy('home-page')


class CreateCourseView(LoginRequiredMixin, CreateView):
    model = NewCourse
    form_class = CourseCreationForm
    template_name = 'lector_create_course.html'
    success_url = reverse_lazy('lector_personal_dashboard')

    def form_valid(self, form):
        # Automatically assign the logged-in user as the author
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditCourseView(LoginRequiredMixin, UpdateView):
    model = NewCourse
    form_class = CourseCreationForm
    template_name = 'lector_edit_course.html'
    success_url = reverse_lazy('lector_personal_dashboard')

    def get_queryset(self):
        # Restrict editing to courses created by the logged-in user
        queryset = NewCourse.objects.filter(author=self.request.user)
        print(f"Queryset for user {self.request.user}: {queryset}")  # Debug statement
        return queryset

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        print(f"Object fetched: {obj}")  # Debug statement
        return obj


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = NewCourse
    template_name = 'lector_course_delete_confirmation.html'

    def get_object(self, queryset=None):
        # Ensure the logged-in user is the author of the course
        queryset = NewCourse.objects.filter(author=self.request.user)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])

    def get_success_url(self):
        # Redirect to the dashboard after deletion
        return reverse_lazy('lector_personal_dashboard')


class LectorCourseDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Fetch the course object based on the pk (primary key)
        course = get_object_or_404(NewCourse, pk=pk, author=request.user)

        # Render the course detail page for the lector
        return render(request, 'lector_course_detail.html', {'course': course})


@csrf_exempt
def upload_textbook(request, pk):
    course = get_object_or_404(NewCourse, pk=pk, author=request.user)
    if request.method == 'POST' and request.FILES.getlist('textbooks'):
        for file in request.FILES.getlist('textbooks'):
            Textbook.objects.create(course=course, file=file)
        # Optionally, set the first uploaded file as the primary textbook
        if not course.textbooks:
            course.textbooks = request.FILES.getlist('textbooks')[0]
            course.save()
    return redirect('lector-course-detail', pk=pk)

@csrf_exempt
def delete_textbook(request, pk):
    textbook = get_object_or_404(Textbook, pk=pk)
    if request.method == 'POST':
        textbook.file.delete()
        textbook.delete()
    return redirect('lector-course-detail', pk=textbook.course.pk)


def all_dashboard(request):
    # Fetch all courses (not filtered by user)
    courses = NewCourse.objects.all()
    return render(request, 'lector_dashboard.html', {'courses': courses})


def view_student_homework(request, course_id, student_id):
    course = get_object_or_404(NewCourse, pk=course_id)
    student = get_object_or_404(CustomUser, pk=student_id)

    # Fetch the student's homework for the specific course
    homeworks = Homework.objects.filter(course=course, student=student)
    has_homework = homeworks.exists()

    # Fetch the student-course relationship and retrieve the score
    student_course = StudentCourse.objects.filter(course=course, student=student).first()
    score = None
    if student_course:
        score = student_course.score
        print(f"Retrieved score for student {student.username} in course {course.title}: {score}")
    print(f"Context passed to template: {{ 'score': {score} }}")

    return render(request, 'student_homework.html', {
        'course': course,
        'student': student,
        'homeworks': homeworks,
        'has_homework': has_homework,
        'score': score,  # Pass the current score to the template
    })

def update_student_score(request, pk, student_pk):
    course = get_object_or_404(NewCourse, pk=pk)
    student = get_object_or_404(CustomUser, pk=student_pk)

    if request.method == 'POST':
        score = request.POST.get('score')

        try:
            # Validate the score
            score = Decimal(score)
        except InvalidOperation:
            score = None  # Handle invalid input gracefully

        if score is not None:
            # Fetch or create the student-course relationship
            student_course, created = StudentCourse.objects.get_or_create(
                student=student, course=course
            )
            # Update the score
            student_course.score = score
            student_course.save()
            print(f"Updated score for {student.username} in course {course.title}: {score}")

    # Redirect to ensure updated data is displayed
    return redirect('view-student-homework', course_id=course.pk, student_id=student.pk)


from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from project3.accounts.models import CustomUser
import os




class NewCourse(models.Model):
    title = models.CharField(max_length=255, verbose_name="Course Title")
    description = models.TextField(verbose_name="Course Description")
    textbooks = models.FileField(upload_to="courses/textbooks/", blank=True, null=True, verbose_name="Textbooks")
    homeworks = models.FileField(upload_to="courses/homeworks/", blank=True, null=True, verbose_name="Homeworks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="new_courses")  # Link to user
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="applied_courses", blank=True)

    def __str__(self):
        return self.title


class Textbook(models.Model):
    course = models.ForeignKey(NewCourse, on_delete=models.CASCADE, related_name="textbook_files")
    file = models.FileField(upload_to="courses/textbooks/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Textbook for {self.course.title} ({self.file.name})"

    @property
    def file_name(self):
        """Extracts just the original file name without the unique suffix."""
        base_name = os.path.basename(self.file.name)
        # Split the name and remove the Django-generated suffix
        original_name = "_".join(base_name.split("_")[:-1])
        return original_name or base_name  # Return the full name if no suffix exists


class Homework(models.Model):
    course = models.ForeignKey(NewCourse, on_delete=models.CASCADE, related_name='homework_files')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='homework_files')
    file = models.FileField(upload_to="courses/homeworks/")
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='uploaded_homeworks')  # Add this field

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

    @property
    def file_name(self):
        """Extracts just the original file name without the unique suffix."""
        base_name = os.path.basename(self.file.name)
        # Split the name and remove the Django-generated suffix
        original_name = "_".join(base_name.split("_")[:-1])
        return original_name or base_name  # Return the full name if no suffix exists


class StudentCourse(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(NewCourse, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.score or 'No Score'}"
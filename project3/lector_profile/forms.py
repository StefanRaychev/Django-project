from django import forms
from .models import NewCourse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from project3.accounts.models import CustomUser


class LectorRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'lector'
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = UsernameField()
    password = forms.CharField(
        strip=False
    )


class ProfileEditForm(UserCreationForm):
    class Meta (UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        exclude = ['password1', 'password2']


class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = NewCourse
        fields = ['title', 'description', 'textbooks', 'homeworks']
        labels = {
            'title': 'Course Title',
            'description': 'Course Description',
            'textbooks': 'Upload Textbooks',
            'homeworks': 'Upload Homeworks',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'textbooks': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'homeworks': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
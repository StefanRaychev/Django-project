from django import forms
from project3.accounts.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user


class StudentLoginForm(AuthenticationForm):
    username = UsernameField()
    password = forms.CharField(
        strip=False
    )


class StudentProfileEditForm(UserCreationForm):
    class Meta (UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        exclude = ['password1', 'password2']

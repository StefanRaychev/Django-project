from django.shortcuts import render


def home(request):
    return render(request, 'home1.html')
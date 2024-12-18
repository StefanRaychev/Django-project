from django.urls import path
from project3.common import views

urlpatterns = [
    path('', views.home, name='home-page'),  # Root URL ("/") points to the home view
]

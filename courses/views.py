from django.shortcuts import render
from .models import Course

def home(request):
    courses = Course.objects
    return render(request, 'courses/home.html', {'courses': courses})

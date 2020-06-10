from django.shortcuts import render
from .models import Course
from django.db.models import F

def home(request):
    courses = Course.objects.order_by('upload_date').reverse()
    return render(request, 'courses/home.html', {'courses': courses})

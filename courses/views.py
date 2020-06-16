from django.shortcuts import render, redirect, HttpResponse
from .models import Course
from django.db.models import Q
from .my_scripts import CourseInfo
import wget
import os

def home(request):
    courses = Course.objects.order_by('upload_date').reverse()
    for course in courses:

        if not course.name:
            obj = CourseInfo(course.url)
            Course.objects.filter(url=course.url).update(name=obj.get_name())

        if not course.rating:
            obj = CourseInfo(course.url)
            Course.objects.filter(url=course.url).update(rating=obj.get_rating())

        if not course.platform:
            obj = CourseInfo(course.url)
            Course.objects.filter(url=course.url).update(platform=obj.get_platform())

        if not course.image:
            obj = CourseInfo(course.url)
            Course.objects.filter(url=course.url).update(image=obj.get_image())

    return render(request, 'courses/home.html', {'courses': courses})


def search(request):
    template = 'courses/search.html'
    query = request.GET.get('search')
    query = query.strip("'").strip('"')
    results = Course.objects.filter(Q(name__contains=query) | Q(category__contains=query))
    return render(request, 'courses/search.html', {'courses': results, 'query': query})



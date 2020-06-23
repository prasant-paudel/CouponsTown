from django.shortcuts import render, redirect, HttpResponse
from .models import Course, Subscriber
from django.db.models import Q
from .my_scripts import CourseInfo


def home(request):
    courses = Course.objects.order_by('upload_date').reverse()
    return render(request, 'courses/home1.html', {'courses': courses})

def info_page(request):
    course_id = request.GET.get('course_id')
    course = Course.objects.get(id=course_id)
    tags = course.tags
    related_courses = Course.objects.filter(Q(tags__contains=tags))
    return render(request, 'courses/info_page.html', {'course': course, 'related_courses': related_courses})

def search(request):
    template = 'courses/home.html'
    query = request.GET.get('search')
    query = str(query).strip("'").strip('"')
    results = Course.objects.filter(Q(name__contains=query) | Q(category__contains=query))
    msg = f'Search results for "{ query}"'
    return render(request, template, {'courses': results, 'message': msg})


def category(request):
    template = 'courses/home.html'
    query = request.GET.get('search')
    query = str(query).strip("'").strip('"')
    results = Course.objects.filter(Q(category__contains=query))
    return render(request, template, {'courses': results})

def subscribe(request):
    email = request.POST.get('email')
    full_name = request.POST.get('full_name')
    
    if not Subscriber.objects.filter(email=email):
        Subscriber.objects.create(full_name=full_name, email=email)
        msg = f"Thank you! {full_name} You've successfully been subscribed as {email}"
    else:
        msg = "The email alerady exists!"

    courses = Course.objects.order_by('upload_date').reverse()

    return render(request, 'courses/home.html', {'message': msg, 'courses': courses})




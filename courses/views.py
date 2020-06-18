from django.shortcuts import render, redirect, HttpResponse
from .models import Course, Subscriber
from django.db.models import Q
from .my_scripts import CourseInfo
import wget
import os

def home(request):
    courses = Course.objects.order_by('upload_date').reverse()
    for course in courses:

        if not course.affiliate_url:
            obj = CourseInfo(course.url)
            Course.objects.filter(url=course.url).update(affiliate_url=obj.affiliate_url)

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

def api(request):
    # query = request.GET.get('query')
    command = request.GET.get('command')
    
    # Check validation i.e. Course is expired or not
    if command == "validate":
        courses = Course.objects.all()
        for course in courses:
            obj = CourseInfo(course.url)
            Course.objects.filter(id=course.id).update(expired=obj.is_expired())
            print(f'Validated  {course.name}')
        return HttpResponse('Course Validation Completed Successfully!')

    # Get Rating for Courses
    if command == 'update_ratings':
        courses = Course.objects.all()
        for course in courses:
            obj = CourseInfo(course.url)
            Course.objects.filter(id=course.id).update(rating=obj.get_rating())
            print(f'Rating Updated for  {course.name},  {obj.get_rating()}')
        return HttpResponse('Course Ratings Updated Successfully!')

    return HttpResponse(f'Successful Ineraction!')


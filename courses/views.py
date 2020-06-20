from django.shortcuts import render, redirect, HttpResponse
from .models import Course, Subscriber
from django.db.models import Q
from .my_scripts import CourseInfo
import wget
import os

def home(request):

    from django.http import HttpRequest
    print('\n\n', HttpRequest.headers, '\n\n')

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
        
        if not course.duration:
            obj = CourseInfo(course.url)
            Course.objects.filter(url=course.url).update(duration=obj.get_duration())

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

    # Update Affiliate URLs
    if command == 'update_affiliate_urls':
        courses = Course.objects.all()
        for course in courses:
            obj = CourseInfo(course.url)
            Course.objects.filter(id=course.id).update(affiliate_url=obj.affiliate_url)
            print(f'Affiliate URLs Updated for {course.url}')
        return HttpResponse('Affiliate URLs Updated Successfully!')

    # Update Images
    if command == 'update_images':
        courses = Course.objects.all()
        for course in courses:
            if 'udemy' in str(course.url).lower():
                obj = CourseInfo(course.url)
                Course.objects.filter(id=course.id).update(image=obj.get_image())
                print(f'Image Updated for {course.name}')
            else:
                print(f'\n\nNot Udemy{course.image.url}')
        return HttpResponse('Images Updated Successfully!')

    if command == 'update_durations':
        courses = Course.objects.all()
        for course in courses:
            if 'udemy' in str(course.url).lower():
                print(f'Fetching Duration for {course.name}')
                obj = CourseInfo(course.url)
                Course.objects.filter(id=course.id).update(duration=obj.get_duration())
                
            if 'eduonix' in str(course.url).lower():
                print(f'Fetching Duration for {course.name}')
                obj = CourseInfo(course.url)
                Course.objects.filter(id=course.id).update(duration=obj.get_duration())
            
        return HttpResponse('\nDuration Updated Successfully!')

    return HttpResponse(f'Successful Ineraction!')


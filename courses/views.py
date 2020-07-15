from django.shortcuts import render, redirect, HttpResponse, Http404
from .models import Course, Subscriber, RealDiscount
from django.db.models import Q
from .my_scripts import CourseInfo
from .tags_scraper import TagScraper
import pickle


def home(request):
    courses = Course.objects.order_by('upload_date').reverse()
    high_rated = Course.objects.order_by('rating')
    high_rated = list(high_rated)[:10]

    try:
        all_small_tags = courses.first().tags.choices
        keys = list(all_small_tags)
        all_tags = [(all_small_tags[x]) for x in keys]
    except AttributeError:
        all_tags = []

    return render(request, 'courses/home.html', {'courses': courses, 'high_rated':high_rated, 'all_tags': all_tags})

def info_page(request):
    _course = request.GET.get('course')
    try:
        course = Course.objects.get(name_encoded=_course)
    except:
        raise(Http404)
    try:
        contents = pickle.loads(course.contents)
    except:
        contents = []

    all_small_tags = course.tags.choices
    keys = list(all_small_tags)
    all_tags = [(all_small_tags[x]) for x in keys] 
    
    related_courses = Course.objects.filter(Q(tags__icontains=course.tags))
    related_courses = list(related_courses)[:10]
    return render(request, 'courses/info_page.html', {'course': course, 'related_courses': related_courses, 'all_tags': all_tags, 'contents':contents})

def search(request):
    template = 'courses/home.html'
    query = request.GET.get('q')
    query = str(query).strip("'").strip('"')

    queryset = query.split()
    results = []
    for q in queryset:
        r = Course.objects.filter(Q(name__icontains=q) | Q(category__icontains=q))
        for i in r:
            if not i in results:
                results.append(i)

    msg = f'Search results for "{query}"'
    return render(request, template, {'courses': results, 'message': msg})


def category(request):
    template = 'courses/home.html'
    query = request.GET.get('search')
    query = str(query).strip("'").strip('"')
    results = Course.objects.filter(Q(category__icontains=query))
    msg = 'Sorry! Page is under Construction.'
    return render(request, template, {'courses': results, 'message': msg})

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


def error_404_view(request, exception):
    return render(request, 'courses/404.html')

from django.shortcuts import HttpResponse, get_object_or_404
import base64
import pickle
from urllib.parse import quote_plus

from courses.models import Course
# from courses.scraper.app import CourseInfo
from courses.scraper.udemy_info_extractor import UdemyInfoExtractor


def apiOverview(request):
    endpoints = {
        'fetch-coupons/': 'Fetch coupons from the internet',
        'validate/<pk>/': 'Check validation of course',
        'update-ratings/': 'Update ratings of all courses',
        'fetch-missing-images/': 'Fetch courses missing images',
        'update-course-info/<pk>/': 'Fetch a course info and update',
        'remove-duplicate-courses/': 'Remove duplicate courses',
        'submit-coupon/<encoded_url>/': 'Add course from course url base64 encoded',
    }

    return HttpResponse('hello world')

def fetch_coupons(request):
    pass


def validate(request, course_url_base64):
    course_url = base64.decodebytes(course_url_base64.encode())
    course = get_object_or_404(Course, url=course_url)

    courseinfo = UdemyInfoExtractor(course.url)
    course.expired = courseinfo.is_free != True
    course.save()


def submit_coupon(request, course_url_base64):
    course_url = base64.decodebytes(course_url_base64.encode()).decode()

    # IF COURSE ALREADY EXISTS
    if Course.objects.filter(url=course_url).exists():
        course = get_object_or_404(Course, url=course_url)
        return HttpResponse(f'[!] Course already exists --> {course.name}')
    else:
        Course.objects.create(url=course_url, category='not_set')
        course = Course.objects.get(url=course_url)

    courseinfo = UdemyInfoExtractor(course_url)

    # check validity
    if not courseinfo.is_free:
        return HttpResponse('[!] Course is invalid or expired')

    course.name = courseinfo.title
    course.category = courseinfo.category
    course.image_url = courseinfo.image_url
    course.description = str(courseinfo.description).encode()
    course.rating = courseinfo.rating
    course.duration = courseinfo.duration
    course.platform = courseinfo.platform
    course.expired = courseinfo.is_free == False

    # Encode name for urls
    course.name_base64 = base64.b64encode(str(course.name).encode()).decode()
    course.name_encoded = quote_plus(course.name)
    course.save()
    
    
    # Fetch Contents / Things You'll Learn
    contents = []
    if contents:
        import pickle
        # print(len(contents))
        course.contents = pickle.dumps(contents)
    
    

    # Save Info
    try:
        course.save()
        print('[+] Course added', course.name)
        return HttpResponse('[+] Course added ' + str(course.name) + '\n')
    except TypeError:
        pass

    return HttpResponse('hello')


def update_info(request, course_url_base64):
    course_url = base64.decodebytes(course_url_base64.encode())
    course = get_object_or_404(course_url)


def list_courses_urls(request):
    courses = ''
    for course in Course.objects.all():
        courses += ' ' + course.url.strip()
    return HttpResponse(courses)

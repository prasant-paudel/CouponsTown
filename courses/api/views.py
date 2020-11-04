from django.shortcuts import HttpResponse, get_object_or_404
import base64
import pickle
from urllib.parse import quote_plus

from courses.models import Course
from courses.scraper.app import CourseInfo

def apiOverview(request):
    enepoints = {
        'validate/<pk>/': 'Check validation of course',
        'update-ratings/': 'Update ratings of all courses',
        'fetch-missing-images/': 'Fetch courses missing images',
        'fetch-course-info/<pk>': 'Fetch a course info and update',
        'remove-duplicate-courses': 'Remove duplicate courses',
        'submit-coupon/<encoded_url>': 'Add course from course url base64 encoded',
    }
    return HttpResponse('hello world')


def validate(request, id):
    course = get_object_or_404(Course, id=id)
    print(course.url)
    
    

def submit_coupon(request, course_url_base64):
    course_url = base64.decodebytes(course_url_base64.encode()).decode()

    if not Course.objects.filter(url=course_url):
        Course.objects.create(url=course_url, category='not_set')
    course = Course.objects.get(url=course_url)
    
    courseinfo = CourseInfo(course_url)

    # Fetch Name
    course.name = courseinfo.get_title()

    # Encode name for urls
    temp_name = base64.b64encode(str(course.name).encode()).decode()
    course.name_base64 = temp_name
    course.save()
    temp_name = quote_plus(course.name)
    course.name_encoded = temp_name
    course.save()

    # Fetch Image
    course.image = courseinfo.get_image()

    # Fetch Contents / Things You'll Learn
    contents = courseinfo.get_content_list()
    if contents:
        import pickle
        # print(len(contents))
        course.contents = pickle.dumps(contents)

    # Fetch Description
    description = courseinfo.get_description()
    if description:
        course.description = str(description).encode()
        # course.save()

    course.rating = courseinfo.get_rating()
    course.duration = courseinfo.get_duration()
    course.platform = courseinfo.platform
    course.expired = False

    # Save Info
    try:
        course.save()
        print('[+] Course added', course.name)
        return HttpResponse('[+] Course added ' + str(course.name) + '\n')
    except TypeError:
        pass

    return HttpResponse('hello')


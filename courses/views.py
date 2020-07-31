from django.shortcuts import render, redirect, HttpResponse, Http404, reverse
from .models import Course, Subscriber, RealDiscount
from django.db.models import Q
from .my_scripts import CourseInfo
from .tags_scraper import TagScraper
import pickle
from django.core.paginator import Paginator, EmptyPage
import pyrebase
from requests.exceptions import ConnectionError

# Production Configuration
config = {
    "apiKey": "AIzaSyCvdtPMemkE6RBh8prl4h0P2kAva9PqLV0",
    "authDomain": "coupons-town.firebaseapp.com",
    "databaseURL": "https://coupons-town.firebaseio.com",
    "projectId": "coupons-town",
    "storageBucket": "coupons-town.appspot.com",
    "messagingSenderId": "511956827149",
    "appId": "1:511956827149:web:2c6f55d2030f27bd9d2944",
    "measurementId": "G-8M4ZXV2J9G",
}
# # Test Configuration
# config = {
#     "apiKey": "AIzaSyAVdH5Qggi8KwUr-iMjBHkxB31reIw52V4",
#     "authDomain": "coupons-town-test.firebaseapp.com",
#     "databaseURL": "https://coupons-town-test.firebaseio.com",
#     "projectId": "coupons-town-test",
#     "storageBucket": "coupons-town-test.appspot.com",
#     "messagingSenderId": "205056322149",
#     "appId": "1:205056322149:web:a3a72b83a638ff88f0b48c",
#     "measurementId": "G-575527J5PG",
# }

def get_queryset(keywords_list):
    _results = []
    for q in keywords_list:
        r = Course.objects.filter(Q(name__icontains=q) | Q(category__icontains=q))
        try:
            r = r.exclude(name=course.name)
        except:
            pass
        for i in r:
            if not i in _results:
                _results.append(i)
    return _results


def home(request):
    courses = Course.objects.order_by('upload_date').reverse()
    courses = courses.filter(expired=False)
    carousel2 = ((i,e) for (i,e) in enumerate(courses[:20]))

    return render(request, 'courses/home.html', {'courses': courses, 'carousel2':carousel2})

def courses(request):
    cat = request.GET.get('filter')
    cat = str(cat).strip("'").strip('"')
    if cat.lower() == 'udemy' or cat.lower() == 'eduonix':
        courses = Course.objects.filter(Q(platform__icontains=cat))
        msg = cat.capitalize() + ' Coupons'
    else:
        courses = Course.objects.filter(expired=False)
    
    courses = courses.order_by('upload_date').reverse()

    p = Paginator(courses, 9)  # Total no of items per page = 9
    try:
        page_num = int(request.GET.get('page'))
    except:
        page_num = 1

    page = p.page(page_num)  # Items from first page
    total_pages = [x+1 for x in range(p.num_pages)]
    active_page = page_num

    high_rated = Course.objects.filter(expired=False).order_by('rating')
    high_rated = list(high_rated)[:10]

    template = 'courses/courses.html'
    context = {'courses': page, 'total_pages': total_pages, 'active_page': active_page, 'num_pages': p.num_pages, 'high_rated':high_rated}
    return render(request, template, context)


def info_page(request):
    _course = request.GET.get('course')
    try:
        course = Course.objects.filter(Q(name=_course) | Q(name_base64=_course) | Q(name_encoded=_course)).first()
        if not course:
            raise(Http404)
    except:
        raise(Http404)
    try:
        contents = pickle.loads(course.contents)
    except:
        contents = []
    
    # Related Courses
    keys = course.name.split()
    results = get_queryset(keys)
    related_courses = list(results)[:10]

    # Category - Web Development
    keys = ['web', 'html', 'css', 'js', 'javascript', 'bootstrap', 'react', 'angular', 'vue', 'php']
    web_development = get_queryset(keys)[:8]
    # Category - Programming
    keys = ['python', 'javascript', 'java', 'programming', 'ruby', 'angular', 'react', 'vue', 
        'flutter', 'android studio', 'sdk', 'swift', 'php', 'algorithm']
    programming = get_queryset(keys)[:8]
    # Category - Office & Productivity
    keys = ['office', 'word', 'excel', 'powerpoint', 'ms access', 'microsoft access', 'tally', 
        'gmail', 'google docs', 'google drive', 'evernote', 'google classroom', 'onedrive', 'youtube',
        'google sites', 'trello', 'powerapps', 'slack', 'wordpress', 'business analysis', 'gsuite', 'trademark',
        'blazor', 'blogging', 'animated promo', 'google photos', 'office 365', 'google drawings', 'jamboard', 
        'sap', 'power bi', 'schedule', 'business', 'communication', 'kubernetes', 'linux']
    office = get_queryset(keys)[:8]
    # Category - Network Security and Ethical Hacking
    keys = ['ethical hacking', 'cybersecurity', 'cyber security', 'pentesting', 'penetration testing', 
        'malware', 'nework security', 'wireshark', 'social engineering', 'deep web', 'dark web', 'kali',
        'linux', 'operating system', 'debugger', 'bug bounty', 'shell', 'scripting', 'oscp', 'ceh', 'cisco',
        'ccna', 'ccnp', 'ccie','comptia', 'routing & switching', 'routing and switching', 'subnetting', 'ipv4', 
        'ipv6', 'python', 'javascript']
    hacking = get_queryset(keys)[:8]
    # Category - Server and Cloud Computing
    keys = ['azure', 'aws' 'google cloud', 'cloud', 'windows server', 'server', 'red hat', 'centos', 'open suse',
        'oracle', 'vm', 'vmware', 'microservices', 'power bi', 'elastic beanstalk', 'ec2', 'route 53',
        'powershell', 'system center', 'devops', 'docker', 'big data', 'hadoop']
    cloud = get_queryset(keys)[:8]


    return render(request, 'courses/info_page.html', {
        'course': course, 'related_courses': related_courses, 'contents':contents,
        'web_development': web_development, 'programming': programming,
        'office': office, 'hacking': hacking, 'cloud': cloud,
    })


def search(request):
    template = 'courses/courses.html'
    query = request.GET.get('q')
    query = str(query).strip("'").strip('"')

    keywordset = query.split()
    results = []
    # Using whole string
    _r = Course.objects.filter(Q(name__icontains=query))
    for i in _r:
        if not i in results:
            results.append(i)
    # Using OR operation to the splitted string
    for q in keywordset:
        _r = Course.objects.filter(Q(name__icontains=q) | Q(category__icontains=q))
        _r = _r.filter(expired=False)
        for i in _r:
            if not i in results:
                results.append(i)

    p = Paginator(results, 9)  # Total no of items per page = 9
    try:
        page_num = int(request.GET.get('page'))
    except:
        page_num = 1

    page = p.page(page_num)  # Items from first page
    total_pages = [x+1 for x in range(p.num_pages)]
    active_page = page_num

    high_rated = Course.objects.filter(expired=False).order_by('rating')
    high_rated = list(high_rated)[:10]


    msg = f'Search results for "{query}"'
    return render(request, template, {'courses': page, 'message': msg, 'total_pages': total_pages, 'active_page': active_page, 'num_pages': p.num_pages, 'high_rated': high_rated})


def category(request):
    cat = request.GET.get('filter')
    cat = str(cat).strip("'").strip('"')
    if cat.lower() == 'udemy' or 'eduonix':
        results = Course.objects.filter(Q(platform__icontains=cat))
        results = results.order_by('upload_date').reverse()
        results = results.order_by('expired').reverse()
        msg = cat.capitalize() + ' Coupons'
    else:
        msg = 'Sorry! Page is under Construction.'

    template = 'courses/courses.html'
    context = {'courses': results, 'message': msg}
    return render(request, template, context)


def subscribe(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    # email = 'user@domain'
    # username = 'user'
    
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()

    # Add user if not exists
    all_users = db.child('users').get()
    for _user in all_users.each():
        _email = _user.val()['email']
        if _email.lower() == email.lower():
            email_exists = True
            return HttpResponse('Email Already Exists')
    if not email_exists:
        _data = {'username': username, 'email': email}
        db.child('users').push(_data)
        return HttpResponse(f'Subscribes Successfully {_email, email}')

    # return render(request, 'courses/courses.html', {'message': msg, 'courses': courses})
    return HttpResponse('hello')

def error_404_view(request, exception):
    return render(request, 'courses/404.html')


def test(request):
    return render(request, 'courses/test.html')


def show_coupons(request):
    courses = Course.objects.filter(expired=False).order_by('upload_date')
    string = 'All Coupons<br>------------------<br>'
    for course in courses:
        # link = 'https://couponstown.me/info-page/?course=' + course.name_encoded
        link = course.url

        string += link + '<br>'
    return HttpResponse(string)


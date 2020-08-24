from django.shortcuts import render, redirect, HttpResponse, Http404, reverse, get_object_or_404
from .models import Course, Subscriber, RealDiscount
from django.db.models import Q
from .my_scripts import CourseInfo
from .tags_scraper import TagScraper
import pickle
from django.core.paginator import Paginator, EmptyPage
import pyrebase
from requests.exceptions import ConnectionError
from fcm_django.models import FCMDevice
from django.views.decorators.csrf import csrf_protect
import requests

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

#=============================================================================#
all_courses = Course.objects.all()
valid_courses = all_courses.filter(expired=False)
expired_courses = all_courses.filter(expired=True)
udemy_courses = all_courses.filter(url__icontains='Udemy').filter(expired=False)
eduonix_courses = all_courses.filter(url__icontains='Eduonix').filter(expired=False)

context = {'all_courses':all_courses, 'valid_courses':valid_courses, 'expired_courses':expired_courses,
    'udemy_courses':udemy_courses, 'eduonix_courses':eduonix_courses}
#=============================================================================#

# Category - Web Development
web_development_wordlist = ['web', 'html', 'css', 'js', 'javascript', 'bootstrap', 'react', 'angular', 'vue', 'php']
# Category - Programming
programming_wordlist = ['python', 'javascript', 'java', 'programming', 'ruby', 'angular', 'react', 'vue', 
    'flutter', 'android studio', 'sdk', 'swift', 'php', 'algorithm']
# Category - Office & Productivity
office_and_productivity_wordlist = ['office', 'word', 'excel', 'powerpoint', 'ms access', 'microsoft access', 'tally', 
    'gmail', 'google docs', 'google drive', 'evernote', 'google classroom', 'onedrive', 'youtube',
    'google sites', 'trello', 'powerapps', 'slack', 'wordpress', 'business analysis', 'gsuite', 'trademark',
    'blazor', 'blogging', 'animated promo', 'google photos', 'office 365', 'google drawings', 'jamboard', 
    'sap', 'power bi', 'schedule', 'business', 'communication', 'kubernetes', 'linux']
# Category - Network Security and Ethical Hacking
network_security_and_ethical_hacking_wordlist = ['ethical hacking', 'cybersecurity', 'cyber security', 'pentesting', 'penetration testing', 
    'malware', 'nework security', 'wireshark', 'social engineering', 'deep web', 'dark web', 'kali',
    'linux', 'operating system', 'debugger', 'bug bounty', 'shell', 'scripting', 'oscp', 'ceh', 'cisco',
    'ccna', 'ccnp', 'ccie','comptia', 'routing & switching', 'routing and switching', 'subnetting', 'ipv4', 
    'ipv6', 'python', 'javascript']
# Category - Server and Cloud Computing
server_and_cloud_computing_wordlist = ['azure', 'aws' 'google cloud', 'cloud', 'windows server', 'server', 'red hat', 'centos', 'open suse',
    'oracle', 'vm', 'vmware', 'microservices', 'power bi', 'elastic beanstalk', 'ec2', 'route 53',
    'powershell', 'system center', 'devops', 'docker', 'big data', 'hadoop', 'kubernetes']
# Category - Photography & Design
photography_and_design_wordlist = ['adobe', 'photoshop', 'drawing', 'painting', 'lightroom', 'coreldraw', 'blender', 'movami', 'flimora', 'premire', 
    'design', 'power director', 'cyberlink', 'gimp', 'inkscape', 'sketch', 'figure', 'infographics', 'ambigram',
    'sculptris', 'brochure templates', 'how to draw', 'water colors', 'canva', 'figma', 'pixologics', 'cartoon', 'whitepapers',
    'illustrator', 'autocad', 'flash', 'design', 'photograph', 'photography', 'video editing']
# Category Business and Marketing
business_and_marketing_wordlist = ['business', 'marketing', 'market', 'financial analysis', 'finance', 'power bi', 'stock marketing',
    'stock trading', 'investing', 'pmp', 'project management', 'pmbok', 'tableau', 'forex', 'financial', 'agle', 'scrum', 'nba', 
    'amazon fba',]
# Category - Health and Fitness
health_and_fitness_wordlist = ['health', 'fitness', 'yoga', 'meditation', 'cognitive therapy', 'nutrition', 'therapy', 'herbalism', 'herbs', 
    'food', 'massage', 'pilates', 'dieting', 'weight loss', 'weight gain']
# Category - Music and Creativity
music_and_creativity_wordlist = ['guitar', 'piano', 'flute', 'ukulele', 'harmonium', 'drumset', 'drum set', 'music', 'singing', 'poetry',
    'keyboard instrument', 'dj', 'audio production', 'voice training', 'song']
#=============================================================================#
def get_queryset(keywords_list):
    global all_courses
    _results = []
    for q in keywords_list:
        r = valid_courses.filter(Q(name__icontains=q) | Q(category__icontains=q))
        r = r.order_by('expired').reverse()
        try:
            r = r.exclude(name=course.name)
        except:
            pass
        for i in r:
            if not i in _results:
                _results.append(i)
    return _results

def get_category_context():
    web_development = get_queryset(web_development_wordlist)[:8]
    programming = get_queryset(programming_wordlist)[:8]
    office = get_queryset(office_and_productivity_wordlist)[:8]
    hacking = get_queryset(network_security_and_ethical_hacking_wordlist)[:8]
    cloud = get_queryset(server_and_cloud_computing_wordlist)[:8]
    photography_and_design = get_queryset(photography_and_design_wordlist)[:8]
    category_context = {
        'photography_and_design': photography_and_design, 'web_development': web_development, 
        'office': office, 'hacking': hacking, 'cloud': cloud, 'programming': programming,}
    return category_context
#=============================================================================#
def search_for(query_string):
    keywordset = query_string.split()
    results = []
    # Using whole string
    _r = all_courses.filter(Q(name__icontains=query_string))
    _r = [x for x in _r if x.image]
    for i in _r:
        if not i in results:
            results.append(i)
    # Using OR operation to the splitted string
    for q in keywordset:
        _r = all_courses.filter(Q(name__icontains=q) | Q(category__icontains=q))
        _r = _r.filter(expired=False)
        for i in _r:
            if not i in results:
                results.append(i)
    return results
#=============================================================================#

def home(request):
    global context
    global valid_courses
    courses = valid_courses.order_by('upload_date').reverse()
    _r = [x for x in courses if x.image]
    courses = _r
    carousel2 = ((i,e) for (i,e) in enumerate(courses[:20]))

    template = 'courses/home.html'
    context.update({'courses': courses, 'carousel2':carousel2})
    return render(request, template, context)


def courses(request):
    global context
    msg = 'All Valid Coupons'
    cat = request.GET.get('filter')
    cat = str(cat).strip("'").strip('"')
    q = request.GET.get('q')
    filter = request.GET.get('filter')

    if cat.lower() == 'udemy' or cat.lower() == 'eduonix':
        courses = valid_courses.filter(Q(platform__icontains=cat))
        msg = cat.capitalize() + ' Coupons'
        filter = cat.capitalize()
    elif cat.lower() == 'expired':
        courses = expired_courses.order_by('rating').reverse()
        msg = 'Expired Coupons'
        filter = 'Expired'
    elif q:
        courses = search_for(q)
    else:
        courses = valid_courses
    
    try:
        courses = courses.order_by('upload_date').reverse()
    except:
        pass
    _r = [x for x in courses if x.image]
    courses = _r

    p = Paginator(courses, 9)  # Total no of items per page = 9
    try:
        page_num = int(request.GET.get('page'))
    except:
        page_num = 1

    page = p.page(page_num)  # Items from first page
    total_pages = [x+1 for x in range(p.num_pages)]
    active_page = page_num

    high_rated = valid_courses.order_by('rating')
    high_rated = list(high_rated)[:10]

    if not q:
        q=''

    template = 'courses/courses.html'
    context.update({'courses': page, 'total_pages': total_pages, 'active_page': active_page, 
        'num_pages': p.num_pages, 'high_rated':high_rated, 'filter': filter, 'message':msg, 
        'q':q, 'filter': filter})
    return render(request, template, context)


def coupon_page(request):
    global context
    _course = request.GET.get('course')
    filter = request.GET.get('filter')
    try:
        course = all_courses.get(Q(name=_course) | Q(name_base64=_course) | Q(name_encoded=_course))
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

    

    template = 'courses/coupon_page.html'
    context.update({'course': course, 'related_courses': related_courses, 'contents':contents,'filter': filter,})
    context.update(get_category_context())
    return render(request, template, context)


def info_page(request):
    global context
    _course = request.GET.get('course')
    filter = request.GET.get('filter')
    try:
        course = all_courses.get(Q(name=_course) | Q(name_base64=_course) | Q(name_encoded=_course))
        if not course:
            raise(Http404)
    except:
        raise(Http404)
    try:
        contents = pickle.loads(course.contents)
    except:
        contents = []
    try:
        description = course.description.decode()
    except:
        description = ''
    
    print('\n\n')
    print(description)
    print('\n\n')
    
    
    # Related Courses
    keys = course.name.split()
    results = get_queryset(keys)
    related_courses = list(results)[:10]

    template = 'courses/info_page.html'
    context.update({'course': course, 'related_courses': related_courses,
        'contents':contents, 'description': description, 'filter': filter,})
    return render(request, template, context)


def search(request):
    query = request.GET.get('q')
    redir = reverse('courses') + '?filter=search&q=' + query
    return redirect(redir)


def category(request, category):
    cat = category.strip("'").strip('"')
    if cat=='web-development':
        return HttpResponse(cat)


    template = 'courses/courses.html'
    context.update({'courses': results, 'message': msg})
    return render(request, template, context)


def subscribe(request):
    return redirect('home')


def error_404_view(request, exception):
    global context
    template = 'courses/404.html'
    return render(request, template, context)


def test(request):
    # path('course/<str:anyarg>/', views.courses, 'courses') 
    # return reverse('course', args=[''])
    return render(request, 'courses/test.html')


def show_coupons(request):
    courses = valid_courses.order_by('upload_date')
    string = 'All Coupons<br>------------------<br>'
    for course in courses:
        # link = 'https://couponstown.me/info-page/?course=' + course.name_encoded
        link = course.url
        string += link + '<br>'
    return HttpResponse(string)


def games_giveaways(request):
    template = 'courses/games_giveaways.html'
    return render(request, template)


def submit_coupons(request):
    global context
    msg = 'Want to share coupons with us?'
    name = request.GET.get('name')
    coupon = request.GET.get('coupon')

    if coupon:
        if all_courses.filter(url=coupon).exists():
            msg = 'Sorry! Coupon Already Exists'
        else:
            url = 'http://localhost:8000/api/?command=fetch_single_course_info&coupon=' + coupon
            try:
                resp = requests.get(url)
                msg = 'Thank You For Submitting Coupon <br>' + resp.text.split('] ')[-1]
            except:
                msg = 'Connection Error. Please Try Again'

            course = Course.objects.filter(url=coupon)
            if name and course.exists():
                course.update(uploaded_by=name)

    template = 'courses/submit_coupons.html'
    context.update({'message': msg, 'name': name})
    return render(request, template, context)
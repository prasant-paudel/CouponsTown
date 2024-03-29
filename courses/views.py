from django.shortcuts import render, redirect, HttpResponse, Http404, reverse, get_object_or_404
from .models import Course, Subscriber, RealDiscount
from django.db.models import Q
# from .my_scripts import CourseInfo
import pickle
from django.core.paginator import Paginator, EmptyPage
from requests.exceptions import ConnectionError
from django.views.decorators.csrf import csrf_protect
import requests
import base64

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
#category - Teaching and Academics
teaching_and_academics_wordlist =['engineering','humanities','math', 'science', 'social', 'science', 'biology','algebra','geometry', 'trignometry','calculus','environmental science','education',
    'socilogy','academic','english language','german language','french language','spanish','grammer','learn english','english language','sign language','psychology',
    'social science']

#=============================================================================#
def get_queryset(keywords_list):
    global all_courses
    _results = []
    for q in keywords_list:
        r = valid_courses.filter(Q(name__icontains=q) | Q(category__icontains=q))
        r = r.order_by('expired').reverse()
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
    
    canonical = course.url.split("?")[0]
    
    print('\n\n')
    print(description)
    print('\n\n')
    
    
    # Related Courses
    keys = str(course.name).split()
    results = get_queryset(keys)
    related_courses = list(results)[:10]

    template = 'courses/info_page.html'
    context.update({'course': course, 'related_courses': related_courses,
        'contents':contents, 'description': description, 'filter': filter, 'canonical':canonical})
    return render(request, template, context)


def search(request):
    query = request.GET.get('q')
    redir = reverse('courses') + '?filter=search&q=' + query
    return redirect(redir)


def category(request, category):
    global context
    cat = category.strip("'").strip('"')
    if cat=='web-development':
        results = get_queryset(web_development_wordlist)
        msg = 'Web Development'
    elif cat=='programming':
        results = get_queryset(programming_wordlist)
        msg = 'Programming Language'
    elif cat=='office-and-productivity':
        results = get_queryset(office_and_productivity_wordlist)
        msg = 'Office & Productivity'
    elif cat=='network-security-and-ethical-hacking':
        results = get_queryset(network_security_and_ethical_hacking_wordlist)
        msg = 'Network Security & Ethical Hacking'
    elif cat=='server-and-cloud-computing':
        results = get_queryset(server_and_cloud_computing_wordlist)
        msg = 'Server & Cloud Compting'
    elif cat=='photography-and-design':
        results = get_queryset(photography_and_design_wordlist)
        msg = 'Photography & Design'
    elif cat=='business-and-marketing':
        results = get_queryset(business_and_marketing_wordlist)
        msg = 'Business & Marketing'
    elif cat=='health-and-fitness':
        results = get_queryset(health_and_fitness_wordlist)
        msg = 'Health & Fitness'
    elif cat=='music-and-creativity':
        results = get_queryset(music_and_creativity_wordlist)
        msg = 'Music & Creativity'
    elif cat=='teaching-and-academics':
        results = get_queryset(teaching_and_academics_wordlist)
        msg = 'Teaching & Academics'
    else:
        raise(Http404)
    
    high_rated = valid_courses.order_by('rating')
    high_rated = list(high_rated)[:10]

    template = 'courses/category.html'
    context.update({'courses': results, 'message': msg, 'high_rated':high_rated})
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
            url = f'http://localhost:8000/api/submit-coupon/{base64.encodebytes(coupon.encode()).decode()}'
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    msg = 'Thank You For Submitting Coupon'
            except:
                msg = 'Connection Error. Please Try Again'

            course = Course.objects.filter(url=coupon)
            if name and course.exists():
                course.update(uploaded_by=name)

    template = 'courses/submit_coupons.html'
    context.update({'message': msg, 'name': name})
    return render(request, template, context)

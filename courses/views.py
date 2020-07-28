from django.shortcuts import render, redirect, HttpResponse, Http404, reverse
from .models import Course, Subscriber, RealDiscount
from django.db.models import Q
from .my_scripts import CourseInfo
from .tags_scraper import TagScraper
import pickle
from django.core.paginator import Paginator, EmptyPage


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
        courses = Course.objects.all()
    
    courses = courses.order_by('upload_date').reverse()

    p = Paginator(courses, 9)  # Total no of items per page = 9
    try:
        page_num = int(request.GET.get('page'))
    except:
        page_num = 1

    page = p.page(page_num)  # Items from first page
    total_pages = [x+1 for x in range(p.num_pages)]
    active_page = page_num

    print(page_num)

    high_rated = Course.objects.order_by('rating')
    high_rated = high_rated.filter(expired=False)
    high_rated = list(high_rated)[:10]

    try:
        all_small_tags = Course.objects.first().tags.choices
        keys = list(all_small_tags)
        all_tags = [(all_small_tags[x]) for x in keys]
    except AttributeError:
        all_tags = []

    return render(request, 'courses/courses.html', {'courses': page, 'total_pages': total_pages, 'active_page': active_page, 'num_pages': p.num_pages, 'high_rated':high_rated, 'all_tags': all_tags})


def info_page(request):
    _course = request.GET.get('course')
    try:
        course = Course.objects.filter(Q(name=_course) | Q(name_base64=_course)).first()
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
        for i in _r:
            if not i in results:
                results.append(i)

    high_rated = Course.objects.order_by('rating')
    high_rated = list(high_rated)[:10]

    try:
        all_small_tags = Course.objects.first().tags.choices
        keys = list(all_small_tags)
        all_tags = [(all_small_tags[x]) for x in keys]
    except AttributeError:
        all_tags = []

    msg = f'Search results for "{query}"'
    return render(request, template, {'courses': results, 'message': msg, 'high_rated': high_rated, 'all_tags': all_tags})


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
    full_name = request.POST.get('full_name')
    
    if not Subscriber.objects.filter(email=email):
        Subscriber.objects.create(full_name=full_name, email=email)
        msg = f"Thank you! {full_name} You've successfully been subscribed as {email}"
    else:
        msg = "The email alerady exists!"

    courses = Course.objects.order_by('upload_date').reverse()

    return render(request, 'courses/courses.html', {'message': msg, 'courses': courses})


def error_404_view(request, exception):
    return render(request, 'courses/404.html')


def test(request):
    return render(request, 'courses/test.html')

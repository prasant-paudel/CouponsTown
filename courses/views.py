from django.shortcuts import render, redirect, HttpResponse
from .models import Course
from django.db.models import Q


def home(request):
    courses = Course.objects.order_by('upload_date').reverse()
    return render(request, 'courses/home.html', {'courses': courses})

def search(request):
    template = 'courses/search.html'
    query = request.GET.get('search')
    query = query.strip("'").strip('"')
    results = Course.objects.filter(Q(name__contains=query))
    print('\n\n')
    print(query)
    print('\n\n')

    return render(request, 'courses/search.html', {'courses': results, 'query': query})
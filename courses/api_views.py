from django.shortcuts import HttpResponse
from .models import Course, RealDiscount
from .my_scripts import CourseInfo
import wget
import os
from .coupon_extractor import CouponExtractor
from .tags_scraper import TagScraper

def api(request):
    # query = request.GET.get('query')
    command = request.GET.get('command')
    
    # Check validation i.e. Course is expired or not
    if command == "validate":
        courses = Course.objects.all()
        for course in courses:
            print(f'[+] Validing  {course.name}')
            obj = CourseInfo(course.url)
            Course.objects.filter(id=course.id).update(expired=obj.is_expired())
        return HttpResponse('Course Validation Completed Successfully!')

    # Get Rating for Courses
    if command == 'update_ratings':
        courses = Course.objects.all()
        for course in courses:
            obj = CourseInfo(course.url)
            Course.objects.filter(id=course.id).update(rating=obj.get_rating())
            print(f'[+] Rating Updated for  {course.name},  {obj.get_rating()}')
        return HttpResponse('Course Ratings Updated Successfully!')

    # Update Affiliate URLs
    if command == 'update_affiliate_urls':
        courses = Course.objects.all()
        for course in courses:
            obj = CourseInfo(course.url)
            Course.objects.filter(id=course.id).update(affiliate_url=obj.affiliate_url)
            print(f'[+] Affiliate URLs Updated for {course.url}')
        return HttpResponse('Affiliate URLs Updated Successfully!')

    # Remove Affiliate URLs
    if command == 'remove_affiliate_urls':
        courses = Course.objects.all().update(affiliate_url='')
        return HttpResponse('Affiliate URLs Removed Successfully!')

    # Fetch infomation of courses from the url in Course database table
    if command == 'fetch_course_info_from_url':
        courses = Course.objects.all()
        for course in courses:
            obj = CourseInfo(url=course.url)

            # Fetch Name
            if not course.name:
                print(f'[+] Fetching Name for {course.name}')
                Course.objects.filter(id=course.id).update(name=obj.get_name())

            # Fetch Platform
            if not course.platform:
                print(f'[+] Fetching Platform for {course.name}')
                Course.objects.filter(id=course.id).update(platform=obj.platform)

            # Fetch Rating 
            if not course.rating:
                print(f'[+] Fetching Rating for {course.name}')
                Course.objects.filter(id=course.id).update(rating=obj.get_rating())

            # Fetch Duration
            if not course.duration:
                print(f'[+] Fetching Duration for {course.name}')
                Course.objects.filter(id=course.id).update(duration=obj.get_duration())

            # Fetch Image
            print(f'[+] Fetching Image for {course.name}')
            Course.objects.filter(id=course.id).update(image=obj.get_image())

            # Fetch Tags
            print(f'[+] Fetching Tags for {course.name}')
            try:
                rd = RealDiscount.objects.get(coupon=course.url)
            except:
                continue
                
            ts = TagScraper(rd.offer)
            tags = ts.get_course_tags()
            print(f'{tags}\n')
            # Adding Tags to the database
            Course.objects.filter(id=course.id).update(tags=tags)
            # print(list(course.tags))
            


        print('\n[+] New Courses Deployed Successfully!\n')
        return HttpResponse('New Courses Deployed Successfully!')

    if command == 'update_durations':
        courses = Course.objects.all()
        for course in courses:
            if 'udemy' in str(course.url).lower():
                print(f'[+] Fetching Duration for {course.name}')
                obj = CourseInfo(course.url)
                Course.objects.filter(id=course.id).update(duration=obj.get_duration())
                
            if 'eduonix' in str(course.url).lower():
                print(f'[+] Fetching Duration for {course.name}')
                obj = CourseInfo(course.url)
                Course.objects.filter(id=course.id).update(duration=obj.get_duration())

        return HttpResponse('Duration Updated Successfully!')

    if command == 'fetch_coupons':
        obj =  CouponExtractor(target_url='http://real.discount', target_pattern='/offer/')
        print('\n[+] Crawling website for offer links')
        obj.extract_coupons()
        return HttpResponse('Offers Fetched Successfully!')
 
    # Deploy Coupons from RealDiscount database table
    if command == 'deploy_coupons':
        print('\n[+] Deploying Coupons to the server')
        discounts = RealDiscount.objects.all()
        for discount in discounts:
            # if coupon does not exists in Course database table
            if not Course.objects.filter(url=discount.coupon).exists() and discount.coupon:
                Course.objects.create(url=discount.coupon, category='not_set')
                print('-->', discount.coupon)

        print('\n[+] Coupons Deployed Successfully!\n')
        return HttpResponse('Coupons Deployed Successfully!')
        
    if command == 'filter_existing_urls':
        courses = Course.objects.all()
        for course in courses:
            filtered_url = 'http://' + course.url.split('//')[-1]
            Course.objects.filter(id=course.id).update(url=filtered_url)
            print(f'[+] URL Filtered for {course.name}')
        return HttpResponse('URLs Filtered Successfully!')

    return HttpResponse(f'Successful Ineraction!')
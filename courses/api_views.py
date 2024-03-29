# from django.shortcuts import HttpResponse, reverse
# from django.db.models.query_utils import Q
# from .models import Course, RealDiscount
# # from .my_scripts import CourseInfo
# import wget
# import os
# from .coupon_extractor import CouponExtractor
# # from .tags_scraper import TagScraper
# from base64 import b64encode
# from urllib.parse import quote_plus, urljoin
# import requests


# def api(request):
#     command = request.GET.get('command')
    
#     # Check validation i.e. Course is expired or not
#     if command == "validate":
#         courses = Course.objects.all()
#         for course in courses:
#             obj = CourseInfo(course.url)
#             Course.objects.filter(id=course.id).update(expired=obj.is_expired())
#             if obj.is_expired():
#                 print(f'[-] Expired  {course.name}')
#             else:
#                 print(f'[+] Valid  {course.name}')
#         return HttpResponse('Course Validation Completed Successfully!')

#     # Get Rating for Courses
#     if command == 'update_ratings':
#         courses = Course.objects.all()
#         for course in courses:
#             obj = CourseInfo(course.url)
#             Course.objects.filter(id=course.id).update(rating=obj.get_rating())
#             print(f'[+] Rating Updated for  {course.name},  {obj.get_rating()}')
#         return HttpResponse('Course Ratings Updated Successfully!')

#     # Update Affiliate URLs
#     if command == 'update_affiliate_urls':
#         courses = Course.objects.all()
#         for course in courses:
#             obj = CourseInfo(course.url)
#             Course.objects.filter(id=course.id).update(affiliate_url=obj.affiliate_url)
#             print(f'[+] Affiliate URLs Updated for {course.url}')
#         return HttpResponse('Affiliate URLs Updated Successfully!')

#     # Fetch infomation of courses from the url in Course database table
#     if command == 'fetch_course_info_from_url':
#         courses = Course.objects.all().order_by('upload_date').reverse()
#         for course in courses:
#             print('===>', course.url, '<===')
#             obj = None

#             # Fetch Name
#             if not course.name:
#                 obj = CourseInfo(course.url)
#                 print(f'[+] Fetching Name for {course.name}')
#                 # Course.objects.filter(id=course.id).update(name=obj.get_name())
#                 course.name = obj.get_name()
#                 course.save()

#             # Fetch Image
#             if not course.image:
#                 if not obj:
#                     obj = CourseInfo(course.url)         
#                 print(f'[+] Fetching Image for {course.name}')
#                 # Course.objects.filter(id=course.id).update(image=obj.get_image())
#                 course.image = obj.get_image()
#                 course.save()

#             # if course.name and not (course.name_encoded and course.name_base64):
#             if 1==1:
#                 print(f'[+] Encoding Name {course.name}')
#                 temp_name = b64encode(str(course.name).encode()).decode()
#                 course.name_base64 = temp_name
#                 course.save()
#                 temp_name = quote_plus(course.name)
#                 course.name_encoded = temp_name
#                 course.save()

#             # Fetch Platform
#             if not course.platform:
#                 if not obj:
#                     obj = CourseInfo(course.url)
#                 print(f'[+] Fetching Platform for {course.name}')
#                 # Course.objects.filter(id=course.id).update(platform=obj.platform)
#                 course.platform = obj.platform
#                 course.save()

#             # Fetch Contents / Things You'll Learn
#             if 'udemy.com' in course.url and not (course.contents or course.expired):
#                 if not obj:
#                     obj = CourseInfo(url=course.url)
#                 print(f'[+] Fetching Contents for {course.name}')
#                 contents = obj.get_content_list()
#                 if contents:
#                     import pickle
#                     # print(len(contents))
#                     course.contents = pickle.dumps(contents)
#                     course.save()

#             # Fetch Description
#             # if not course.description:
#             if 1==1:
#                 if not obj:
#                     obj = CourseInfo(url=course.url)
#                 print(f'[+] Fetching Description for {course.name}')
#                 description = obj.get_description()
#                 if description:
#                     course.description = str(description).encode()
#                     course.save()

#             # Fetch Rating 
#             if not (course.rating or course.expired):
#                 if not obj:
#                     obj = CourseInfo(course.url)
#                 print(f'[+] Fetching Rating for {course.name}')
#                 Course.objects.filter(id=course.id).update(rating=obj.get_rating())
#                 # course.rating = obj.get_rating()
#                 # course.save()

#             # Fetch Duration
#             if not (course.duration and course.expired):
#                 if not obj:
#                     obj = CourseInfo(course.url)
#                 print(f'[+] Fetching Duration for {course.name}')
#                 # Course.objects.filter(id=course.id).update(duration=obj.get_duration())
#                 course.duration = obj.get_duration()
#                 course.save()

#             # course.save()

#         print('\n[+] New Courses Deployed Successfully!\n')
#         return HttpResponse('New Courses Deployed Successfully!')

#     # Fetch Single Course Info
#     if command == 'fetch_single_course_info':
#         course_id = request.GET.get('id')
#         coupon = request.GET.get('coupon')
#         if course_id:
#             course = Course.objects.filter(id=course_id).first()
#             obj = CourseInfo(course.url)
#         if coupon:
#             if not Course.objects.filter(url=coupon):
#                 Course.objects.create(url=coupon, category='not_set')
#             course = Course.objects.get(url=coupon)
#             obj = CourseInfo(coupon)

#         # If uploaded by user Remove course with same title if exists
#         if coupon:
#             _old = Course.objects.filter(Q(name=obj.get_name()) & Q(expired=True))
#             print(obj.get_name())
#             if _old.exists():
#                 for _course in _old:
#                     print(_course.name)
#                     _course.delete()
        
#         # Fetch Name
#         print(coupon)
#         course.name = obj.get_name()

#         # Encode name for urls
#         temp_name = b64encode(str(course.name).encode()).decode()
#         course.name_base64 = temp_name
#         course.save()
#         temp_name = quote_plus(course.name)
#         course.name_encoded = temp_name
#         course.save()

#         # Fetch Image
#         course.image = obj.get_image()

#         # Fetch Contents / Things You'll Learn
#         contents = obj.get_content_list()
#         if contents:
#             import pickle
#             # print(len(contents))
#             course.contents = pickle.dumps(contents)

#         # Fetch Description
#         description = obj.get_description()
#         if description:
#             course.description = str(description).encode()
#             # course.save()

#         # Fetch Rating
#         course.rating = obj.get_rating()
#         # Fetch Duration
#         course.duration = obj.get_duration()
#         # Fetch Platform
#         course.platform = obj.platform
#         # Declare Valid
#         course.expired = False

#         # Save Info
#         try:
#             course.save()
#             print('[+] Course added', course.name)
#             return HttpResponse('[+] Course added ' + str(course.name) + '\n')
#         except TypeError:
#             pass

#     if command == 'update_durations':
#         courses = Course.objects.all()
#         for course in courses:
#             if 'udemy' in str(course.url).lower():
#                 print(f'[+] Fetching Duration for {course.name}')
#                 obj = CourseInfo(course.url)
#                 Course.objects.filter(id=course.id).update(duration=obj.get_duration())
                
#             if 'eduonix' in str(course.url).lower():
#                 print(f'[+] Fetching Duration for {course.name}')
#                 obj = CourseInfo(course.url)
#                 Course.objects.filter(id=course.id).update(duration=obj.get_duration())

#         return HttpResponse('Duration Updated Successfully!')

#     if command == 'fetch_coupons':
#         obj =  CouponExtractor(target_url='http://real.discount', target_pattern='/offer/')
#         print('\n[+] Crawling website for offer links')
#         obj.extract_coupons()
#         return HttpResponse('Offers Fetched Successfully!')
 
#     # Deploy Coupons from RealDiscount database table
#     if command == 'deploy_coupons':
#         print('\n[+] Deploying Coupons to the server')
#         discounts = RealDiscount.objects.all()
#         for discount in discounts:
#             # if coupon does not exists in Course database table
#             if not Course.objects.filter(url=discount.coupon).exists() and discount.coupon:
#                 Course.objects.create(url=discount.coupon, category='not_set')
#                 print('-->', discount.coupon)

#         print('\n[+] Coupons Deployed Successfully!\n')
#         return HttpResponse('Coupons Deployed Successfully!')

#     if command == 'filter_existing_urls':
#         courses = Course.objects.all()
#         rd_objs = RealDiscount.objects.all()
#         for course in courses:
#             filtered_url = 'https://' + course.url.split('//')[-1]
#             Course.objects.filter(id=course.id).update(url=filtered_url)
#             print(f'[+] URL Filtered for Course {course.name}')
#         print('')
#         for obj in rd_objs:
#             filtered_url = 'https://' + str(obj.coupon).split('//')[-1]
#             if rd_objs.filter(coupon=filtered_url).exists():
#                 continue
#             else:
#                 obj.coupon = filtered_url
#                 obj.save()
#             print(f'[+] URL Filtered for Offer {obj.offer.split("/offer/")[-1]}')

#         return HttpResponse('URLs Filtered Successfully!')

#     # Compress images > 300 KB
#     if command == 'compress_images':
#         image_dir = 'media/'
#         minimum_original_size = 300000
#         compression_percent = 30

#         from PIL import Image
#         from pathlib import Path

#         images = os.listdir(image_dir)
#         for image in images:
#             image = os.path.join(image_dir, image)
#             # get image size
#             size = Path(image).stat().st_size
#             if size >= minimum_original_size:
#                 # Open image
#                 img = Image.open(image)
#                 x = img.size[0]*compression_percent/100
#                 y = img.size[1]*compression_percent/100
#                 img.convert('RGB')
#                 img = img.resize((int(x),int(y)), Image.ANTIALIAS)
#                 img.save(image, optimize=True, quality=95)
#                 print('[+] Compressed', image)
#                 img.close()

#     if command == 'clear_image_urls_from_db':
#         courses = Course.objects.all()
#         for course in courses:
#             course.image = ''
#             course.save()

#     if command == 'remove_duplicate_courses':
#         courses = Course.objects.all()
#         for course in courses:
#             similar = Course.objects.filter(name=course.name)
#             if len(similar) > 1:
#                 course.delete()

#     if command == 'update_course_contents':
#         print('[+] Updating Course Contents')
#         courses = Course.objects.all()
#         for course in courses:
#             if 'udemy.com' in course.url:
#                 obj = CourseInfo(url=course.url)
#                 contents = obj.get_content_list()
#                 if contents:
#                     import pickle
#                     print(len(contents))
#                     course.contents = pickle.dumps(contents)
#                     course.save()

#     if command == 'scrape_discudemy':
#         from courses.discudemy_scraper import crawl
#         crawl()
#         return HttpResponse(f'Crawling Discudemy')

#     if command == 'update_images':
#         courses = Course.objects.all()
#         for course in courses:
#             try:
#                 url = urljoin('http://localhost:8000/', course.image.url)
#                 print(url)
#                 status = int(requests.get(url).status_code)
#             except:
#                 status = 0
#                 continue
#             if status == 404:
#                 try:
#                     obj = CourseInfo(course.url)
#                     course.image = obj.get_image()
#                     course.save()
#                 except:
#                     pass

#     return HttpResponse(f'Successful Ineraction!')

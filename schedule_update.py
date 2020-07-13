import datetime
import requests
import time

def log(string):
    with open('couponstown.log', 'a') as f:
        f.write(str(string) + '\n')

while 1:
    now = datetime.datetime.now()
    # Every 2 Hour
    if now.hour % 2 == 0 and now.minute == 0:
        print(now)
        # Fetch New Coupons from Internet
        print('[+] Fetching New Courses form Internet')
        requests.get('http://couponstown.me:8000/api/?command=fetch_coupons')

    # Every Hour
    if now.minute == 30:
        # Execute every hour
        pass

    # Every 10 Minutes
    if now.minute % 2 == 0:
        print(now)
        log('[+] Removing Duplicate Courses')
        requests.get('http://couponstown.me:8000/api/?command=remove_duplicate_courses')
        log('[+] Fetching Course info from URLs')
        requests.get('http://couponstown.me:8000/api/?command=fetch_course_info_from_url')
        log('[+] Filtering Existing URLs')
        requests.get('http://couponstown.me:8000/api/?command=filter_existing_urls')
        log('[+] Validating Courses')
        requests.get('http://couponstown.me:8000/api/?command=validate')
        log('[+] Updating Ratings')
        requests.get('http://couponstown.me:8000/api/?command=update_ratings')
    
    time.sleep(1)




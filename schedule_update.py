import datetime
import requests
import time

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
    if now.minute % 10 == 0:
        print(now)
        print('[+] Removing Duplicate Courses')
        requests.get('http://couponstown.me:8000/api/?command=remove_duplicate_courses')
        print('[+] Fetching Course info from URLs')
        requests.get('http://couponstown.me:8000/api/?command=fetch_course_info_from_url')
        print('[+] Validating Courses')
        requests.get('http://couponstown.me:8000/api/?command=validate')
        print('[+] Updating Ratings')
        requests.get('http://couponstown.me:8000/api/?command=update_ratings')
    
    time.sleep(1)




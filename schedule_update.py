import datetime
import requests
import time


def log(string):
    with open('couponstown.log', 'a') as f:
        f.write(f"[{datetime.datetime.now()}] {str(string)} \n")


if __name__ == '__main__':
    while 1:
        now = datetime.datetime.now()
        # Every 2 Hour
            log('[+] Fetching Course info from URLs')
            requests.get('http://couponstown.me:8000/api/?command=fetch_course_info_from_url')

        # Every Hour
        if now.minute == 30:
            # Execute every hour
            pass

        # Every 30 minute
        if now.minute == 10 or now.minute == 40:
            print(now)
            # Fetch New Coupons from Internet
            print('[+] Fetching New Courses form Internet')
            requests.get('http://couponstown.me:8000/api/?command=fetch_coupons')

        # Every 2 Minutes
        if now.minute % 2 == 0:
            print(now)
            log('[+] Removing Duplicate Courses')
            requests.get('http://couponstown.me:8000/api/?command=remove_duplicate_courses')
            log('[+] Filtering Existing URLs')
            requests.get('http://couponstown.me:8000/api/?command=filter_existing_urls')
            log('[+] Validating Courses')
            requests.get('http://couponstown.me:8000/api/?command=validate')
            log('[+] Updating Ratings')
            requests.get('http://couponstown.me:8000/api/?command=update_ratings')

        time.sleep(1)




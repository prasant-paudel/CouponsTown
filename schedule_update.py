from threading import *
import datetime
import time
import requests


def log(string):
    with open('couponstown.log', 'a') as f:
        f.write(f"[{datetime.datetime.now()}] {str(string)} \n")


if __name__ == '__main__':
    while 1:
        try:
            now = datetime.datetime.now()

            def fetch_coupons():
                log('[+] Fetching Coupons from Internet')
                requests.get('http://localhost:8006/api/?command=fetch_coupons')
            
            def update_courses():
                log('[+] Updating Courses info from URLs')
                requests.get('http://localhost:8007/api/?command=fetch_course_info_from_url')
            
            def validate_courses():
                log('[+] Validating Courses')
                requests.get('http://localhost:8008/api/?command=validate')
            
            def filter_urls():
                log('[+] Filtering Existing URLs')
                requests.get('http://localhost:8009/api/?command=filter_existing_urls')

            def update_ratings():
                log('[+] Updating Ratings')
                requests.get('http://localhost:8010/api/?command=update_ratings')
            
            def remove_duplicate():
                log('[+] Removing Duplicate Courses')
                requests.get('http://localhost:8011/api/?command=remove_duplicate_courses')
            
            def scrape_discudemy():
                log('[+] Scraping Discudemy')
                requests.get('http://localhost:8000/api/?command=scrape_discudemy')

            t1 = Thread(target=fetch_coupons)
            t2 = Thread(target=update_courses)
            t3 = Thread(target=validate_courses)
            t4 = Thread(target=filter_urls)
            t5 = Thread(target=update_ratings)
            t6 = Thread(target=remove_duplicate)
            t7 = Thread(target=scrape_discudemy)

            # Every Day
            if now.hour == 0 and now.minute == 7 and now.second == 0:
                t6.start()  # Scrape Discudemy

            # Every 3 Hour
            if now.hour % 3 == 0 and now.minute == 0 and now.second == 0:
                t1.start()  # Fetch New Coupons
                
            # Every 5 Minutes
            if now.minute % 5 == 0 and now.second == 0:
                t2.start()  # Update Courses Info
                t4.start()  # Filter URLs
                t5.start()  # Update Ratings

            # Every Minute
            if now.second == 0:
                t3.start()  # Validate Courses
                t6.start()  # Remove Duplicate Courses
        except (ConnectionError, requests.exceptions.ConnectionError):
            print('[!] Connection Error!')
        finally:
            pass

        time.sleep(1)


from threading import *
import datetime
import time
import requests


def log(string):
    with open('couponstown.log', 'a') as f:
        f.write(f"[{datetime.datetime.now()}] {str(string)} \n")

def fetch_coupons():
    log('[+] Fetching Coupons from Internet')
    try:
        requests.get('http://localhost:8006/api/?command=fetch_coupons')
    except (ConnectionError, requests.exceptions.ConnectionError):
        log('[!] Connection Error!')
    finally:
        pass


def update_courses():
    log('[+] Updating Courses info from URLs')
    try:
        requests.get('http://localhost:8007/api/?command=fetch_course_info_from_url')
    except (ConnectionError, requests.exceptions.ConnectionError):
        log('[!] Connection Error!')
    finally:
        pass

def validate_courses():
    log('[+] Validating Courses')
    try:
        requests.get('http://localhost:8008/api/?command=validate')
    except (ConnectionError, requests.exceptions.ConnectionError):
        log('[!] Connection Error!')
    finally:
        pass

def filter_urls():
    log('[+] Filtering Existing URLs')
    try:
        requests.get('http://localhost:8009/api/?command=filter_existing_urls')
    except (ConnectionError, requests.exceptions.ConnectionError):
        log('[!] Connection Error!')
    finally:
        pass

def update_ratings():
    log('[+] Updating Ratings')
    try:
        requests.get('http://localhost:8010/api/?command=update_ratings')
    except (ConnectionError, requests.exceptions.ConnectionError):
        log('[!] Connection Error!')
    finally:
        pass

def remove_duplicate():
    log('[+] Removing Duplicate Courses')
    try:
        requests.get('http://localhost:8011/api/?command=remove_duplicate_courses')
    except (ConnectionError, requests.exceptions.ConnectionError):
        log('[!] Connection Error!')
    finally:
        pass

def scrape_discudemy():
    log('[+] Scraping Discudemy')
    try:
        requests.get('http://localhost:8000/api/?command=scrape_discudemy')
    except (ConnectionError, requests.exceptions.ConnectionError):
        log('[!] Connection Error!')
    finally:
        pass


t1 = Thread(target=fetch_coupons)
t2 = Thread(target=update_courses)
t3 = Thread(target=validate_courses)
t4 = Thread(target=filter_urls)
t5 = Thread(target=update_ratings)
t6 = Thread(target=remove_duplicate)
t7 = Thread(target=scrape_discudemy)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()


if __name__ == '__main__':
    threads = [t1, t2, t3, t4, t5, t6, t7]
    while 1:
        try:
            for _t in threads:
                if not _t.is_alive():
                    _t.join()


        except (ConnectionError, requests.exceptions.ConnectionError):
            print('[!] Connection Error!')
        finally:
            pass

        time.sleep(0.9)


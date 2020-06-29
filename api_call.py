import requests
import os
import time

help = '''
1. Fetch Coupons from Internet
2. Deploy Coupons Fetched from Internet
3. Filter Existing Course URLs
4. Fetch Course Info from Course URLs
5. Update Expired Courses (Validate Courses)
6. Update Ratings
7. Update Affiliate URLs
8. Remove Affiliate URLs
9. Update Course Durations
10.
11. Main Menu
'''


def switch(opt, server):
    if opt == 1:
        resp = requests.get(f'http://{server}/api/?command=fetch_coupons')
    elif opt == 2:
        resp = requests.get(f'http://{server}/api/?command=update_ratings')
    elif opt == 3:
        resp = requests.get(f'http://{server}/api/?command=filter_existing_urls')
    elif opt == 4:
        resp = requests.get(f'http://{server}/api/?command=fetch_course_info_from_url')
    elif opt == 5:
        resp = requests.get(f'http://{server}/api/?command=validate')
    elif opt == 6:
        resp = requests.get(f'http://{server}/api/?command=deploy_coupons')
    elif opt == 7:
        resp = requests.get(f'http://{server}/api/?command=update_affiliate_urls')
    elif opt == 8:
        resp = requests.get(f'http://{server}/api/?command=remove_affiliate_urls')
    elif opt == 9:
        resp = requests.get(f'http://{server}/api/?command=update_durations')
    elif opt == 10:
        resp = requests.get(f'http://{server}/api/?command=remove_duplicate_courses')
    elif opt == 11:
        raise Exception('Back to Main Menu')
    else:
        print('[-] Invalid Range!')
    print(resp.text)
    time.sleep(5)

def take_int():
    while 1:
        opt = input('Select Option > ')
        # Filter Input
        try:
            return int(opt)
        except:
            print('[-] Invalid Input!')
            take_int()


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

while 1:
    # Select Server
    print('''
    1. LocalHost
    2. CourseHub
    3. CourseHub 8000
    ''')
    opt = take_int()
    if opt == 1:
        server = '127.0.0.1:8000'
    elif opt == 2:
        server = 'coursehub.ddns.net:80'
    elif opt == 3:
        server = 'coursehub.ddns.net:8000'
    else:
        print('[-] Invalid Range!')
        continue
    
    while 1:
        # Clear Screen
        clear_screen()

        # API Menu
        print('\n========', server, '========')
        print(help)
        value = take_int()
        try:
            switch(value, server)
        except Exception as msg:
            print(msg)
            break


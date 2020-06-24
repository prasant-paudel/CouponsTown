import requests
from bs4 import BeautifulSoup


def is_expired(course_url):
    response = requests.get(course_url)
    parsed_html = BeautifulSoup(response.text)

    # Eduonix Pricing Div
    if 'eduonix.com' in course_url:
        pricing = parsed_html.findAll('div', {'id': 'scrollTp'})

    # Udemy Pricing Div
    elif 'udemy.com' in course_url:
        pricing = parsed_html.findAll('div', {'class': 'buy-box'})

    else:
        pricing = 'not compatible platform'

    # Checking Price
    if 'enroll now' in str(pricing).lower():
        return False
    return True



if __name__ == '__main__':
    url1 = 'https://www.eduonix.com/courses/Web-Development/Learn-PHP-and-MySQL-Development-By-Building-Projects?utm_source=realdiscount&utm_medium=referral&utm_campaign=Sagar'
    url2 = 'https://www.udemy.com/course/aws-certified-developer-associate-masterclass/?couponCode=A86BF8215E4C16678A93'
    url3 = 'http://www.eduonix.com/courses/Web-Development/Become-A-Certified-Web-Developer-From-Scratch?utm_source=realdiscount&utm_medium=referral&utm_campaign=Sagar'
    print(is_expired(url1), is_expired(url2), is_expired(url3))

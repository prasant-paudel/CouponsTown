import requests
from bs4 import BeautifulSoup
import re
import os
import wget

class CourseInfo:
    def __init__(self, url):
        self.url = url
        self.affiliate_url = 'http://adf.ly/23576813/' + url.strip('"').strip("'").split('//')[-1]
        self.platform = str(url).split('//')[-1].split('/')[0].lower()

        self.response = requests.get(url)
        self.parsed_html = BeautifulSoup(self.response.content)

    def get_name(self):
        return self.parsed_html.findAll('h1')[0].get_text()

    def get_rating(self):
        return re.findall('(?:.*>)(\d\.\d)', self.response.text)[0]
    
    def get_image(self):
        if 'udemy' in str(self.platform).lower():
            remote_img_url = self.parsed_html.findAll('img')[1].attrs['src']
            temp_img = f".temp/{remote_img_url.split('/')[-1]}"
            if not os.path.exists('.temp'):
                os.mkdir('.temp')
            if not os.path.exists(temp_img):
                wget.download(remote_img_url, temp_img)
            return temp_img
        return 'courses/static/images/no-image.svg'

    def get_platform(self):
        return self.url.strip('"').strip("'").split('//')[-1].split('/')[0].split('www.')[-1].split('.')[0].capitalize()

    def is_best_seller(self):
        if 'bestseller' in str(self.parsed_html).lower():
            return True
        return False

    def is_expired(self):
        response = requests.get(self.url)
        parsed_html = BeautifulSoup(response.text, features='lxml')

        # Eduonix Pricing Div
        if 'eduonix.com' in self.url:
            pricing = parsed_html.findAll('div', {'id': 'scrollTp'})
        
        # Udemy Pricing Div
        elif 'udemy.com' in self.url:
            pricing = parsed_html.findAll('div', {'class': 'buy-box'})
        
        else:
            pricing = 'not compatible platform'
        
        # Checking Price
        if 'enroll now' in str(pricing).lower():
            return False
        return True

    def get_rating(self):
        # Rating Container for Udemy
        if 'udemy.com' in self.url:
            rating_container = self.parsed_html.findAll('span', {'class': 'tooltip-container'})

        # Rating Container for Eduonix
        elif 'eduonix.com' in self.url:
            rating_container = self.parsed_html.findAll('span', {'class': 'rating-text ratingValues'})

        else:
            rating_container = "Nothing Appropriate!"

        # Extracting Rating 
        rating = re.findall('\w\.\w', str(rating_container))[0]
        return rating

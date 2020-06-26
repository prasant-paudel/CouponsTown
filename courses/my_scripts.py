import requests
from bs4 import BeautifulSoup
import re
import os
import wget
from .models import RealDiscount

class CourseInfo:
    def __init__(self, url, page_source=None):
        self.url = url
        self.page_source = page_source
        self.affiliate_url = 'http://adf.ly/23576813/' + url.strip('"').strip("'").split('//')[-1]
        self.platform = self.url.split('//')[-1].split('/')[0].split('www.')[-1].split('.')[0].capitalize()
        
        ob = RealDiscount.objects.get(coupon=self.url)
        self.offer_url = ob.offer
        
        if self.page_source:
            self.parsed_html = BeautifulSoup(self.page_source)
        else:
            self.response = requests.get(url)
            self.parsed_html = BeautifulSoup(self.response.content)

    def get_name(self):
        try:
            return self.parsed_html.findAll('h1')[0].get_text().strip()
        except:
            return ''

    # def get_rating(self):
    #     return re.findall('(?:.*>)(\d\.\d)', self.response.text)[0]
    
    def get_image(self):
        if self.platform == 'Udemy':
            remote_img_url = self.parsed_html.findAll('img')[1].attrs['src']
        else:
            page_src = requests.get(self.offer_url).content
            parsed = BeautifulSoup(page_src)
            remote_img_url = parsed.findAll('img')[0]['src']
            
            
        img_name = self.get_name()
        # Filtering Name
        img_name = img_name.strip().replace(' ', '_')
        img_name = img_name.replace('/', '-').replace('\\', '-')
        img_name = img_name.replace('"', '_').replace('|', '_')

        temp_img = f"media/{img_name}.jpg"
        if not os.path.exists('media'):
            os.mkdir('media')
        if not os.path.exists(temp_img):
            wget.download(remote_img_url, temp_img)
        return temp_img
        
        # print('[-] Image Not Found!')
        # return 'images/no-image.svg'

    def get_platform(self):
        return self.url.strip('"').strip("'").split('//')[-1].split('/')[0].split('www.')[-1].split('.')[0].capitalize()

    def is_best_seller(self):
        if 'bestseller' in str(self.parsed_html).lower():
            return True
        return False

    def is_expired(self):
        # Eduonix Pricing Div
        if 'eduonix.com' in self.url:
            pricing = self.parsed_html.findAll('div', {'id': 'scrollTp'})
        
        # Udemy Pricing Div
        elif 'udemy.com' in self.url:
            pricing = self.parsed_html.findAll('div', {'class': 'buy-box'})
        
        else:
            pricing = 'not compatible platform'

        # Checking Price
        if 'enroll now' in str(pricing).lower():
            print('--> Valid')
            return False
        print('--> Expired')
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
        try:
            rating = re.findall('\w\.\w', str(rating_container))[0]
            return rating
        except:
            return '00'

    def get_duration(self):
        # For exuonix
        if 'eduonix.com' in str(self.url).lower():
            try:
                info_div = self.parsed_html.findAll('div', {'class': 'col-md-12 mt-2'})[0]
                duration = re.findall('(?:</i> )(.*hours?)', str(info_div))[0].strip()
                return duration
            except:
                pass
        # For Udemy
        elif 'udemy.com' in str(self.url).lower():
            try:
                info_div = self.parsed_html.findAll('span', {'data-purpose': 'video-content-length'})[0].get_text()
                if 'mins' in str(info_div):
                    duration = re.findall(".*mins", str(info_div))[0]
                    return duration
                try:
                    duration = re.findall(".*hours", str(info_div))[0]
                except:
                    duration = re.findall(".*hour", str(info_div))[0]
                return duration
            except Exception as msg:
                print(f"Udemy exception while updating duration \n{msg}\n")
                pass
        return 'N/A'


        




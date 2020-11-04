import requests
from bs4 import BeautifulSoup
import os
import wget

class CourseInfo:

    def __init__(self, course_url):
        
        self.course_url = course_url
        self.platform = self.course_url.split('//')[-1].split('/')[0].split('www.')[-1].split('.')[0].capitalize()

        try:
            resp = requests.get(course_url)
        except Exception as e:
            resp = e
            print(e)

        self.parsed_html = BeautifulSoup(resp.text)


    def is_expired(self, retry=4) -> bool:

        course_url = self.course_url
        parsed_html = self.parsed_html

        # FOR UDEMY
        if 'udemy.com' in course_url:
            pricing1 = parsed_html.findAll('div', {'class': 'buy-box'})
            pricing2 = parsed_html.findAll('div', {'class': 'heading'})
            pricing = str(pricing1) + str(pricing2)
        
            if 'enroll now' in pricing.lower():
                return False
            return True


    def get_content_list(self, retries=5):
        contents = []
        url = self.course_url
        parsed_html = self.parsed_html

        # FOR UDEMY
        if 'udemy.com' in url.lower():
            lists = parsed_html.findAll('span', {"class": "what-you-will-learn--objective-item--ECarc"})
            if not lists:
                print('[-] No Content Found')
                return ''
            if retries > 0 and not lists:
                lists = self.get_content_list(retries-1)
            
            for item in lists:
                contents.append(item.get_text())

            return contents


    def get_description(self):
        parsed_html = self.parsed_html
        description = ''
        try:
            description = parsed_html.findAll('div', {'data-purpose': \
                'safely-set-inner-html:description:description'})[0]
        except (AttributeError, IndexError):
            print('[-] Description Not Found')
        finally:
            pass
        return description


    def get_title(self):
        try:
            if 'eduonix.com' in self.course_url:
                return self.parsed_html.findAll('h1', {'class': 'productTopHeading'})[0].get_text().strip()
            return self.parsed_html.findAll('h1')[0].get_text().strip()
        except:
            return ''


    def get_image(self):
        if 'udemy.com' in self.course_url:
            remote_img_url = self.parsed_html.findAll('img')[1].attrs['src']
        else:
            offer_url = RealDiscount.objects.get(coupon=self.course_url).offer
            r = requests.get(offer_url)
            parsed_offer = BeautifulSoup(r.content)
            remote_img_url = parsed_offer.findAll('img')[0]['src']

        img_name = self.get_title()
        # Filtering Name
        img_name = img_name.strip().replace(' ', '_').replace('"', '_')
        img_name = img_name.replace('/', '-').replace('\\', '-')
        img_name = img_name.replace('(', '_').replace(')', '_')

        temp_img = f"media/{img_name}.jpg"
        if not os.path.exists('media'):
            os.mkdir('media')
        if not os.path.exists(temp_img):
            wget.download(remote_img_url, temp_img)
        return temp_img


    def get_rating(self):
        # Rating Container for Udemy
        if 'udemy.com' in self.course_url:
            rating_container = self.parsed_html.findAll('span', {'class': 'tooltip-container'})

        # Rating Container for Eduonix
        elif 'eduonix.com' in self.course_url:
            rating_container = self.parsed_html.findAll('span', {'class': 'rating-text ratingValues'})

        else:
            rating_container = "Nothing Appropriate!"

        # Extracting Rating 
        try:
            rating = re.findall('\w\.\w', str(rating_container))[0]
            return float(rating)
        except:
            return float('00')


    def get_duration(self):
        # For exuonix
        if 'eduonix.com' in str(self.course_url).lower():
            try:
                info_div = self.parsed_html.findAll('div', {'class': 'col-md-12 mt-2'})[0]
                duration = re.findall('(?:</i> )(.*hours?)', str(info_div))[0].strip()
                return duration
            except:
                pass
        # For Udemy
        elif 'udemy.com' in str(self.course_url).lower():
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






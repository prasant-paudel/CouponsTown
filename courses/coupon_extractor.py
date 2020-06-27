# Extracts coupon and writes to database
import requests
from bs4 import BeautifulSoup
import re
import os
from .models import RealDiscount, Course
from django.db.utils import IntegrityError
from .my_scripts import CourseInfo

class CouponExtractor:
    def __init__(self, target_url, target_pattern):
        self.target_url = target_url
        self.target_pattern = target_pattern
        self.links_list = []
        self.coupon_count = 0

    def request(self, url):
        url = url.strip()
        response = requests.get(url)
        return response

    def extract_links(self, url=None):
        '''
        url ==> target url to extract links from
        list_object ==> list object to store extracted links
        pattern ==> pattern to search in link before writing into file
        '''
        if not url:
            url = self.target_url
        page_source = self.request(url).content
        parsed_html = BeautifulSoup(page_source)
        domain = self.target_url.split('//')[-1].split('/')[0]

        print('')
        print('Extracting Links from ' + url)
        print('')

        a_tags = parsed_html.findAll('a')
        for a in a_tags:
            try:
                link = str(a['href'])
                if link[:4] == 'http' and domain in url:
                    if not link in self.links_list:
                        self.links_list.append(link)
                        # if offer page found
                        if self.target_pattern in link:  # link == offer
                            offer_page_source = self.request(link).content
                            # if offer is already expired
                            if 'Expired' in str(offer_page_source):
                                continue
                            # If Offer does not exist in database
                            if not RealDiscount.objects.filter(offer=link).exists():
                                # Extract Coupon from offer link and filter Coupon
                                coupon = self.course_url_from(offer_page_source)
                                coupon = 'http://' + coupon.split('//')[-1]
                                # Validate Coupon
                                if not self.expired(coupon):
                                    self.coupon_count += 1
                                    # Store offer link in database
                                    try:
                                        RealDiscount.objects.create(offer=link, coupon=coupon)
                                        RealDiscount.objects.filter(offer=link).update(valid=True)
                                        Course.objects.create(url=coupon, category='not_set')
                                    except IntegrityError:
                                        self.coupon_count -= 1
                                        continue
                                else:
                                    RealDiscount.objects.filter(offer=link).update(valid=True)

                                print('[+]',self.coupon_count, link)
                                
                                # Update Platform
                                platform = coupon.split('//')[-1].split('www.')[-1].split('.')[0].capitalize()
                                RealDiscount.objects.filter(offer=link).update(platform=platform)

            except KeyError:
                pass
            except KeyboardInterrupt:
                return self.links_list
        return self.links_list

    # Crawling each of the links for more links recursively
    def extract_coupons(self):
        # Create Initial Set of Links to Crawl
        self.extract_links()
        
        try:
            for link in self.links_list:
                print(f'[+] Scanning {link}')
                self.extract_links(link)
        except KeyboardInterrupt:
            print('\n[-] Stopping Crawler')
        except requests.exceptions.ConnectionError:
            print('\n[-] Connection Error!')
        except IndexError:
            pass

    def course_url_from(self, offer_page_source):
        parsed_html = BeautifulSoup(offer_page_source)
        course_url = parsed_html.findAll('a', {'class': 'btn'})[0]['href']
        return course_url.strip()

    def expired(self, course_url):
        response = self.request(course_url)
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
    ob = CouponExtractor(target_url='http://real.discount', target_pattern='/offer/')
    ob.extract_coupons()
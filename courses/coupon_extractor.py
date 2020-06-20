import requests
from bs4 import BeautifulSoup
import re

class CouponExtractor:
    def __init__(self, target_url, target_pattern):
        self.target_url = target_url
        self.target_pattern = target_pattern
        self.links_list = []
        self.offers_links_file = 'extracted_links.txt'
        self.coupons_file = 'coupons.txt'

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
        parsed_html = BeautifulSoup(page_source, features='lxml')
        domain = self.target_url.split('//')[-1].split('/')[0]

        print('')
        print('Extracting Links from ' + self.target_url)
        print('')

        a_tags = parsed_html.findAll('a')
        for a in a_tags:
            try:
                link = str(a['href'])
                if link[:4] == 'http' and domain in url:
                    if not link in self.links_list:
                        #print(link)
                        self.links_list.append(link)
                        if self.target_pattern in link:
                            with open(self.offers_links_file, 'a') as outfile:
                                print(link)
                                outfile.write(str(link) + '\n')
            except KeyError:
                pass
        return self.links_list


    # Crawling each of the links for more links
    def crawl(self):
        self.extract_links()
        try:
            for link in self.links_list:
                print(f'\nScanning {link}')
                self.extract_links(link)
        except KeyboardInterrupt:
            pass

    def course_url_from(self, offer_page_url):
        page_source = self.request(offer_page_url).content
        parsed_html = BeautifulSoup(page_source, features='lxml')
        course_url = parsed_html.findAll('a', {'class': 'btn'})[0]['href']
        return course_url.strip()


    def extract_coupons(self):
        try:
            _temp_offers_list = []
            # Read offer links from file
            with open(self.offers_links_file, 'r') as offer_links:
                for offer in offer_links:
                    if offer not in _temp_offers_list:
                        _temp_offers_list.append(offer)
                        # Extract coupon link from offer
                        coupon = self.course_url_from(offer)

                        # Validate Coupon
                        if not self.expired(coupon):            
                            # Write valid coupon to a file
                            with open(self.coupons_file, 'a') as outfile:
                                outfile.write(coupon + '\n')
                                print(coupon)
        except KeyboardInterrupt:
            pass

    def expired(self, course_url):
        response = self.request(course_url)
        parsed_html = BeautifulSoup(response.text, features='lxml')

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
    ob.crawl()
    ob.extract_coupons()

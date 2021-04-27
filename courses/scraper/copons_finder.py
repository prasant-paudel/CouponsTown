import re
import requests


class Scraper:
    def __init__(self, url=None, page_source=None):
        """
        * You can give url for the website to be scraped 
          or you can give page source in the string format.

        Features:
        * Get all meta tags
        * Get all urls
        """
        self.page_source = page_source
        if not page_source:
            self.page_source = requests.get(url).text

    def get_all_meta(self):
        """Get all <meta> tags from a webpage"""
        regex = '(<meta.*?>)'
        metas = re.findall(regex, self.page_source)
        return metas

    def get_all_urls(self, target_url=None):
        """Get all URLs present in a webpage"""
        regex = '(?:href=")(.*?)"'
        if target_url:
            temp_urls = re.findall(regex, requests.get(target_url).text)
        else:
            temp_urls = re.findall(regex, self.page_source)
        # filter extracted urls
        urls = []
        [urls.append(x) for x in temp_urls if x not in urls]
        return urls


class MetaParser:
    def __init__(self, meta: str):
        self.meta = meta

    def get(self, element: str):
        """
        Get elements in meta tags like name, description, property, etc.
        """
        regex = f'(?:{element}=")(.*?)"'
        elements = re.findall(regex, self.meta)
        if elements:
            return elements[0]
        return None


class DiscudemyScraper:
    def __init__(self):
        self.urls = []
        self.coupons = []

    def __load_coupons_from(self, filename):
        try:
            with open(filename) as f:
                self.coupons = [x.strip() for x in f.readlines()]
        except FileNotFoundError:
            pass

    def recursive_scrape(self, start_page=0, output_file="udemy_coupons.txt", max_retries=10):
        if not self.coupons:
            self.__load_coupons_from(output_file)

        start_page += 1
        coupons_before_scraping = len(self.coupons)
        print("scraping page", start_page)
        sc = Scraper(f"https://discudemy.com/all/{start_page}")
        links = sc.get_all_urls()
        for link in links:
            if not link in self.urls:
                self.urls.append(link)
                _link = "https://www.discudemy.com/go/" + link.split("/")[-1]
                _urls = sc.get_all_urls(_link)
                for x in _urls:
                    if not "discudemy.com" in x:
                        if "udemy.com" in x:
                            print(f"[{len(self.coupons)}] {x}")
                            if x in self.coupons:
                                break
                            else:
                                with open(output_file, 'a') as f:
                                    self.coupons.append(x)
                                    f.write(x + '\n')

        coupons_after_scraping = len(self.coupons)
        if (coupons_before_scraping == coupons_after_scraping):
            max_retries -= 1

        if max_retries > 0:
            self.recursive_scrape(start_page, output_file, max_retries)


if __name__ == '__main__':
    a = DiscudemyScraper()
    a.recursive_scrape()

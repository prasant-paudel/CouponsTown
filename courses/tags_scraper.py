import requests
from bs4 import BeautifulSoup

class TagScraper:
    def __init__(self, url):
        self.url = str(url).strip()
        self.course_tags = []
        self.all_tags = []
        
        self.page_source = requests.get(self.url).content
        self.parsed_html = BeautifulSoup(self.page_source)

    def get_course_tags(self):
        links = self.parsed_html.findAll('a')
        for link in links:
            text = link.get_text()
            if '/offer_cat/' in str(link):
                self.all_tags.append(text)
                if '/search-page/' in str(link):
                    self.course_tags.append(text)
        return self.course_tags



if __name__ == '__main__':
    url = 'https://www.real.discount/offer/ultimate-linux-learning-path/'
    ob = TagScraper(url)
    print(ob.course_tags)














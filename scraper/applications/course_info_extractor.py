# Extracts Courses Info
# requires course url

import requests
import time
import lxml.html


def get_page_source(target_url: str, num_retries=10, delay_sec=5):
    try:
        resp = requests.get(target_url)
        return resp.content
    except:
        if num_retries==0:
            return ''
        print(f"[-] Connection Error!  {target_url}")
        time.sleep(delay_sec)
        get_page_source(target_url, num_retries - 1)


def xpath_content(xpath: str, lxml_doc: str) -> str:
    try:
        return lxml_doc.xpath(xpath)[0]
    except IndexError:
        return ''


class UdemyCourse:
    
    def __init__(self, course_url: str):
        self.course_url = course_url
        self.page_source = get_page_source(course_url)
        self.lxml_doc = lxml.html.fromstring(self.page_source)

    def is_free(self) -> bool:
        # Xpath for Enroll Now button
        xpath_1 = '//*[@id="udemy"]/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/a/text()'
        xpath_2 = '//*[@id="udemy"]/div[1]/div[3]/div[1]/div[3]/div/div/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[5]/div/button/span/text()'
        xpath_3 = '//*[@id="udemy"]/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/button/span/text()'
        xpath_4 = '//*[@id="udemy"]/div[1]/div[3]/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/button/span'

        if 'enroll now' in xpath_content(xpath_1, self.lxml_doc).lower():
            return True
        if 'enroll now' in xpath_content(xpath_2, self.lxml_doc).lower():
            return True
        if 'enroll now' in xpath_content(xpath_3, self.lxml_doc).lower():
            return True
        if 'enroll now' in xpath_content(xpath_4, self.lxml_doc).lower():
            return True

        all_spans = self.lxml_doc.xpath('//span/text()')
        for i, span in enumerate(all_spans):
            # span = lxml.html.tostring(span).decode()
            if span.strip().lower() == 'current price':
                current_price = all_spans[i+1].strip()
                # print('Price -->', current_price)
                if current_price.lower() == 'free':
                    return True

        return False
    
    def get_title(self) -> str:
        # Xpath for title
        xpath_1 = '//*[@id="udemy"]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[1]/h1/text()'
        xpath_2 = '//*[@id="udemy"]/div[1]/div[3]/div[1]/div[4]/div/div/div[4]/div/div[1]/div[1]/h1/text()'
        
        title = xpath_content(xpath_1, self.lxml_doc)
        if not title:
            title = xpath_content(xpath_2, self.lxml_doc)

        return title


if __name__ == '__main__':
    url = "https://www.udemy.com/course/how-to-make-full-responsive-website-using-bootstrap-4/"
    # url = "https://www.udemy.com/course/the-python-programming-v39-comprehensive-bootcamp/?couponCode=5FDFB61B8BCC5552A6BE"
    a = UdemyCourse(course_url=url)
    print(a.is_free())
    print(a.get_title())


import requests
import re
import json

class Course:
    def __init__(self, course_dict):
        self.id = course_dict['id']
        self.url = course_dict['url']
        self.title = course_dict['title'],
        self.subtitle = course_dict['subtitle']
        self.image_url = course_dict['image_url']
        self.rating = course_dict['rating'],
        self.rating_count = course_dict['rating_count']
        self.student_count = course_dict['student_count']
        self.duration = course_dict['duration']
        self.is_free = course_dict['is_free']
        self.language = course_dict['language']
        self.authors = course_dict['authors']
        self.description = course_dict['description']
        self.audience_type = course_dict['audience_type']
        self.category = course_dict['category']


class UdemyInfoExtractor:
    def __scrape_with_regex(self, regex, string):
        things = re.findall(regex, string)
        if things:
            return things[0]
        return None

    def __init__(self, url):
        print('====> Extracting Info: ', url, '<====')
        self.url = url
        self.page_source = requests.get(url).text
        self.subtitle = self.__scrape_with_regex(
            '(?:<meta name="description" content=")(.*?)">', self.page_source)
        self.duration = self.__scrape_with_regex(
            '(?:content_length_text&quot;:&quot;)(.*?)&', self.page_source)
        self.student_count = self.__scrape_with_regex(
            r'(?:num_students&quot;:)(\d*?),&quot', self.page_source)
        self.raw_info = json.loads(self.__scrape_with_regex(
            r'(?:<script type="application/ld\+json">\s)(.*])', self.page_source))[0]
        self.title = self.raw_info['name']
        self.id = self.raw_info['@id']
        self.is_free = self.raw_info['isAccessibleForFree']
        self.rating = self.raw_info['aggregateRating']['ratingValue']
        self.rating_count = self.raw_info['aggregateRating']['ratingCount']        
        self.image_url = self.raw_info['image']
        self.language = self.raw_info['inLanguage']
        self.description = self.__scrape_with_regex('(?:Description</h2>)(.*?)(?:<button type="button" class="udlite-btn)', self.page_source)
        self.audience_type = self.raw_info['audience']['audienceType']
        self.category = self.raw_info['about']['name']
        self.authors = [x['name'] for x in self.raw_info['creator']]
        self.is_always_free = self.is_free and '?couponCode=' not in self.url
        self.platform = self.url.split('://')[-1].split('www.')[-1].split('.com')[0].capitalize()

        self.dict = {
            "url": self.url,
            "title": self.title,
            "id": self.id,
            "subtitle": self.subtitle,
            "duration": self.duration,
            "is_free": self.is_free,
            "is_always_free": self.is_always_free,
            "student_count": self.student_count,
            "rating": self.rating,
            "rating_count": self.rating_count,
            "language": self.language,
            "category": self.category,
            "audience_type": self.audience_type,
            "authors": self.authors,
            "image_url": self.image_url,
            "description": self.description
        }

        self.course = Course(self.dict)


    
    


if __name__ == "__main__":
    a = UdemyInfoExtractor('https://www.udemy.com/course/a-beginners-guide-to-android-app-development/?couponCode=FREEMAR4')
    print(a.course.authors)
    print(a.description)


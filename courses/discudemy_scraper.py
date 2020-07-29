# Discudemy Coupon Scraper

from bs4 import BeautifulSoup
import requests

coupons = []
links = []

def crawl(target_url='https://discudemy.com/all'):
    try:
        page_source = requests.get(target_url).text
    except KeyboardInterrupt:
        exit()
    except:
        return links
    parsed_page = BeautifulSoup(page_source)

    a_tags = parsed_page.findAll('a')
    
    for a in a_tags:
        try:
            link = a['href']
            link = str(link).split('//')[-1].split('www.')[-1]
            link = 'https://' + link
            if 'category/debug' not in link.lower() and link not in links:
                if 'udemy.com' in link.lower():
                    if not 'discudemy.com' in link.lower():
                        if not link in coupons:
                            coupons.append(link)
                            print('\n[+]', link, '\n')
                            # Update Couponstown Server
                            resp = requests.get(f'http://localhost:8000/api/?command=fetch_single_course_info&coupon={link}')
                            print(resp)
                    else:
                        links.append(link)
                        print('-->', link)
                        crawl(link)
        except KeyError:
            pass
    return links

if __name__ == '__main__':
    crawl('https://discudemy.com/all')
    print(len(links))
    print(len(coupons))

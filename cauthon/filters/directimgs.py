# -*- coding: utf-8 -*-
'''
Scrape image galleries which link directly to images
'''
import urlparse
import bs4

IMAGE_TYPES = (
    'jpg', 'jpeg', 'gif', 'png', 'tiff',
    'wmv', 'mpg', 'mpeg', 'avi',
)


def __virtual__():
    return True


def scrape(crawler, url):
    '''
    Retreive the URL by whatever means is appropriate
    '''
    result, parser = crawler.fetch(url)  # pylint: disable=unused-variable
    return extract_photos(url, result.content)


def extract_photos(url, code):
    '''
    Extract the photos and return URLs for them
    '''
    ret = []
    soup = bs4.BeautifulSoup(code, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        comps = link.get('href', '').split('.')
        if comps[-1].lower() in IMAGE_TYPES:
            href = urlparse.urljoin(url, link['href'])
            ret.append(href)
    return ret

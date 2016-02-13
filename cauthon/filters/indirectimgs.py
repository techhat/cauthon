# -*- coding: utf-8 -*-
'''
Scrape image galleries which link directly to images
'''
import re
import urlparse
import bs4

IMAGE_TYPES = (
    'jpg', 'jpeg', 'gif', 'png', 'tiff',
    'wmv', 'mpg', 'mpeg', 'avi',
)

NUM_LINK = re.compile(r'\/\d+\.htm', re.IGNORECASE)
NUM_IMG = re.compile(r'\/[_\d]+\.({0})'.format('|'.join(IMAGE_TYPES)), re.IGNORECASE)


def __virtual__():
    return True


def scrape(crawler, url):
    '''
    Retreive the URL by whatever means is appropriate
    '''
    result, parser = crawler.fetch(url)  # pylint: disable=unused-variable

    ret = set()
    soup = bs4.BeautifulSoup(result.content, 'html.parser')
    links = soup.find_all('a')
    img_pgs = []
    for link in links:
        href = link.get('href', '')
        href = urlparse.urljoin(url, href)
        if NUM_LINK.search(href):
            img_pgs.append(href)

    for page in img_pgs:
        page_result = crawler.session.request(
            'GET',
            page,
            proxies=crawler.proxies,
        )
        page_parser = bs4.BeautifulSoup(page_result.content, 'html.parser')
        imgs = page_parser.find_all('img')
        for img in imgs:
            src = img.get('src', '')
            src = urlparse.urljoin(url, src)
            if NUM_IMG.search(src):
                ret.add(src)

    return list(ret)

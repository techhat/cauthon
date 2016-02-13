# -*- coding: utf-8 -*-
'''
Detect which type of filter to use
'''
import re
import urlparse
import bs4

IMAGE_TYPES = (
    'jpg', 'jpeg', 'gif', 'png', 'tiff',
    'wmv', 'mpg', 'mpeg', 'avi',
)

NUM_LINK = re.compile(r'\/\d+.html')


def __virtual__():
    return True


def scrape(crawler, url):
    '''
    Detect the filter type
    '''
    result, parser = crawler.fetch(url)  # pylint: disable=unused-variable
    urlparser = urlparse.urlparse(url)
    imgs = []
    img_pgs = []
    soup = bs4.BeautifulSoup(result.content, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        href = link.get('href', '')
        href = urlparse.urljoin(url, href)
        comps = href.split('.')
        if comps[-1].lower() in IMAGE_TYPES:
            imgs.append(href)
        if NUM_LINK.search(href):
            img_pgs.append(href)

    if len(imgs) > 0:
        return 'directimgs', urlparser.netloc

    if len(img_pgs) > 0:
        return 'indirectimgs', urlparser.netloc

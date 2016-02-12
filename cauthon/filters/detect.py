# -*- coding: utf-8 -*-
'''
Detect which type of filter to use
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
    Detect the filter type
    '''
    result, parser = crawler.fetch(url)  # pylint: disable=unused-variable
    urlparser = urlparse.urlparse(url)
    imgs = []
    soup = bs4.BeautifulSoup(result.content, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        comps = link.get('href', '').split('.')
        if comps[-1].lower() in IMAGE_TYPES:
            href = urlparse.urljoin(url, link['href'])
            imgs.append(href)

    if len(imgs) > 0:
        return 'directimgs', urlparser.netloc

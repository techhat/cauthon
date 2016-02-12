# -*- coding: utf-8 -*-
'''
Execution module for running Cauthon on Salt minions
'''

try:
    import cauthon
    HAS_CAUTHON = True
except ImportError:
    HAS_CAUTHON = False


def __virtual__():
    '''
    Make sure Cauthon is able to load
    '''
    return HAS_CAUTHON


def scrape(url, module=None):
    '''
    Scrape a site, return the links
    '''
    crawler = cauthon.Crawler()
    return crawler.scrape(url, module)


def download(url):
    '''
    Download the links for a site
    '''
    crawler = cauthon.Crawler()
    return crawler.download(url)

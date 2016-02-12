# -*- coding: utf-8 -*-
'''
Execution module for running Cauthon on Salt minions
'''
from __future__ import absolute_import

try:
    import cauthon
    HAS_CAUTHON = True
except ImportError:
    HAS_CAUTHON = False

__virtualname__ = 'cauthon'


def __virtual__():
    '''
    Make sure Cauthon is able to load
    '''
    if HAS_CAUTHON:
        return __virtualname__
    return False


def scrape(url, module=None):
    '''
    Scrape a site, return the links
    '''
    crawler = cauthon.Crawler(node_type='minion')
    return crawler.scrape(url, module)


def download(url):
    '''
    Download the links for a site
    '''
    crawler = cauthon.Crawler()
    return crawler.download(url)

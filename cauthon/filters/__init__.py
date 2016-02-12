# -*- coding: utf-8 -*-
'''
Cauthon Library
'''
import os
import os.path
import urlparse
import yaml
import salt.syspaths
import salt.utils
import salt.config
from salt.loader import LazyLoader
import cauthon.config


class Filters(object):  # pylint: disable=too-few-public-methods
    '''
    Main connection object for Cauthon
    '''
    def __init__(self, conf_path=None, opts=None):
        if conf_path is None:
            conf_path = '/etc/cauthon'
        if opts:
            self.opts = opts
        else:
            self.opts = cauthon.config.load_config('{0}/cauthon'.format(conf_path))
        self.filters = self._filters()

    def _filters(self, functions=None, whitelist=None):
        '''
        Get a list of installed filters
        '''
        codedir = os.path.dirname(os.path.realpath(__file__))
        return LazyLoader(
            [codedir],
            self.opts,
            tag='filters',
            pack={
                '__filters__': functions,
                '__opts__': self.opts,
            },
            whitelist=whitelist,
        )

    def _func(self, crawler, fun, url, module=None):  # pylint: disable=no-self-use
        '''
        Shortcut to return the function for a URL
        '''
        parsed = urlparse.urlparse(url)
        domain = parsed.netloc
        if module is None:
            crawler.sitemap_load()
            if domain not in crawler.site_map:
                # Try to detect the filter to use, and add to the site map
                new_filt, domain = self.filters['detect.scrape'](crawler, url)
                crawler.sitemap_append(domain, new_filt)
            module = crawler.site_map[domain]
        return '{0}.{1}'.format(module, fun)

    def scrape(self, crawler, url, module=None):
        '''
        Scrape a URL
        '''
        func = self._func(crawler, 'scrape', url, module)
        return self.filters[func](crawler, url)

# -*- coding: utf-8 -*-
'''
Cauthon Library
'''
from __future__ import absolute_import, print_function
import os
import time
import shutil
import urlparse
import cookielib
import yaml
import requests
import bs4
import cauthon.config
import salt.utils

from cauthon.database import Database
from cauthon.filters import Filters

DEFAULT_AGENT = 'Cauthon/0.1.0'


class Crawler(object):
    '''
    Connection object for Cauthon
    '''
    def __init__(self, node_type=None, conf_path=None, opts=None):
        '''
        Set up main class
        '''
        if conf_path is None:
            conf_path = '/etc/cauthon'
        if opts:
            self.opts = opts
        else:
            self.opts = cauthon.config.load_config(
                '{0}/cauthon'.format(conf_path),
            )

        header_dict = {}
        header_dict['User-agent'] = self.opts.get('user-agent', DEFAULT_AGENT)

        self.session = requests.Session()
        self.session.auth = self.opts.get('auth', None)
        self.session.verify = self.opts.get('verify_ssl', True)
        self.session.headers.update(header_dict)

        cookie_jar = self.opts.get(
            'cookie_jar', '/var/cache/cauthon/cookies.txt'
        )
        self.session.cookies = cookielib.LWPCookieJar(cookie_jar)
        if not os.path.isfile(cookie_jar):
            self.session.cookies.save()
        self.session.cookies.load()

        self.proxies = self.opts.get('proxies', {})
        self.base_dir = self.opts.get('base_dir', '/var/cache/cauthon/sites')

        self.db = Database()  # pylint: disable=invalid-name
        self.db.connect(self.opts.get('db_driver', 'sqlite3'))

        self.sitemap_load()
        self.filters = Filters()

    def sitemap_load(self):
        '''
        Load the site.map into self.site_map
        '''
        sitemap_file = self.opts.get('site_map', '/etc/cauthon/site.map')
        with salt.utils.fopen(sitemap_file, 'r') as sm_:
            self.site_map = yaml.safe_load(sm_)

    def sitemap_append(self, domain, fname):
        '''
        Load the site.map into self.site_map
        '''
        sitemap_file = self.opts.get('site_map', '/etc/cauthon/site.map')
        self.site_map[domain] = fname
        with salt.utils.fopen(sitemap_file, 'w') as sm_:
            yaml.dump(self.site_map, sm_, default_flow_style=False)

    def fetch(self,  #pylint: disable=too-many-arguments
              url,
              method='GET',
              params=None,
              data=None,
              force=False,
              req_kwargs=None):
        '''
        Fetch a URL and stash in a database as necessary
        '''
        if req_kwargs is None:
            req_kwargs = {}

        content = None
        cached = False
        if force is False:
            data = self.db.client.execute(
                'SELECT content FROM sites WHERE url = ?', (url,)
            )
            row = data.fetchone()
            if row:
                content = row[0]
                cached = True

        if content is None:
            result = self.session.request(
                method,
                url,
                params=params,
                data=data,
                proxies=self.proxies,
                **req_kwargs
            )
        else:
            result = ReqHook(content)

        parser = bs4.BeautifulSoup(result.content, 'html.parser')
        title = parser.find_all('title')[0].contents[0]

        if not cached:
            self.db.insert(
                'sites',
                url,
                result.content,
                title,
                str(int(time.time())),
            )

        return result, parser

    def scrape(self, url, module=None):
        '''
        Scrape a URL and collect some links
        '''
        return self.filters.scrape(self, url, module)

    def download(self, url):
        '''
        Download the links returned by scrape()
        '''
        print('Downloading {0}'.format(url))
        for link in self.filters.scrape(self, url):
            stream = requests.get(link, stream=True)
            urlparser = urlparse.urlparse(link)
            comps = urlparser.path.split('/')
            out_path = os.path.join(
                self.base_dir,
                urlparser.netloc,
                *comps[:-1]
            )
            try:
                os.makedirs(out_path)
            except OSError:
                pass
            out_file = os.path.join(self.base_dir, urlparser.netloc, *comps)
            if not os.path.exists(out_file):
                print('Saving {0}'.format(link))
                with salt.utils.fopen(out_file, 'w') as fh_:
                    stream.raw.decode_content = True
                    shutil.copyfileobj(stream.raw, fh_)


class ReqHook(object):  # pylint: disable=too-few-public-methods
    '''
    Simulate requests, for data that was stored in the cache
    '''
    def __init__(self, data):
        self.content = data

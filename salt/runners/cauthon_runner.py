# -*- coding: utf-8 -*-
'''
Runner module for running Cauthon on the Salt master
'''
from __future__ import absolute_import, print_function
import pprint
import random
import salt.client
from salt.exceptions import SaltClientError

try:
    import cauthon
    from cauthon.database import Database
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


def _client(opts=None):
    '''
    Get a client connection to Salt
    '''
    if opts is None:
        opts = __opts__['conf_file']
    return salt.client.get_local_client(opts)


def scan_workers():
    '''
    Scan the Salt network for workers
    '''
    ret = {}
    client = _client()
    worker_db = Database()  # pylint: disable=invalid-name
    worker_db.connect(
        'sqlite3',
        '/var/cache/cauthon/workers.sqlite',
        table='workers',
        schema=_worker_schema(),
    )
    try:
        minions = client.cmd(
            '*',
            'grains.item',
            arg=('enable_cauthon'),
            timeout=__opts__['timeout'],
        )
        for minion in minions:
            pprint.pprint(minion)
            data = worker_db.client.execute(
                'SELECT * FROM workers WHERE id = ?', (minion,)
            )
            row = data.fetchone()
            if not row:
                worker_db.insert(
                    'workers',
                    minion,
                )
    except SaltClientError as client_error:
        print(client_error)
        return ret


def _get_worker():
    '''
    Grab a worker from the database
    '''
    method = __opts__.get('cauthon_worker_algorithm', 'random')
    worker_db = Database()  # pylint: disable=invalid-name
    worker_db.connect(
        'sqlite3',
        '/var/cache/cauthon/workers.sqlite',
        table='workers',
        schema=_worker_schema(),
    )
    data = worker_db.client.execute(
        'SELECT id FROM workers'
    )
    rows = data.fetchall()
    idx = random.randint(0, len(rows) - 1)
    worker = rows[idx][0]
    return worker


def scrape(url, module=None, local=False):
    '''
    Scrape a site, return the links
    '''
    if local:
        crawler = cauthon.Crawler(node_type='master')
        return crawler.scrape(url, module)
    else:
        salt_client = _client()
        worker = _get_worker()
        minions = salt_client.cmd(
            worker,
            'cauthon.scrape',
            kwarg={
                'url': url,
                'module': module,
            },
            timeout=__opts__['timeout'],
        )
        return minions[worker]


def download(url):
    '''
    Download the links for a site
    '''
    crawler = cauthon.Crawler()
    return crawler.download(url)


def _worker_schema():
    '''
    Return the schema for the worker database
    '''
    return '''CREATE TABLE workers (
        id text
    )
    '''

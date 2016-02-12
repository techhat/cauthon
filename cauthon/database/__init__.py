# -*- coding: utf-8 -*-
'''
Cauthon Database Library
'''
import os
import os.path
import yaml
import salt.syspaths
import salt.utils
import salt.config
from salt.loader import LazyLoader
import cauthon.config


class Database(object):
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
        self.databases = self._databases()

    def _databases(self, functions=None, whitelist=None):
        '''
        Get a list of installed filters
        '''
        codedir = os.path.dirname(os.path.realpath(__file__))
        return LazyLoader(
            [codedir],
            self.opts,
            tag='databases',
            pack={
                '__databases__': functions,
                '__opts__': self.opts,
            },
            whitelist=whitelist,
        )

    def connect(self, driver, conn_str=None, **kwargs):
        '''
        Connect to a DB
        '''
        func = '{0}.connect'.format(driver)
        self.client = self.databases[func](conn_str, **kwargs)  # pylint: disable=attribute-defined-outside-init
        self.driver = driver  # pylint: disable=attribute-defined-outside-init
        return self.client

    def insert(self, table, *args):
        '''
        Connect to a DB
        '''
        func = '{0}.insert'.format(self.driver)
        self.databases[func](self.client, table, *args)

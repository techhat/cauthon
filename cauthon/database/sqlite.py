# -*- coding: utf-8 -*-
'''
SQLite3 Driver for Cauthon
'''
from __future__ import absolute_import
import sqlite3
from sqlite3 import OperationalError

__virtualname__ = 'sqlite3'


def __virtual__():
    return __virtualname__


def connect(conn_str=None, table='sites', schema=None, **kwargs):
    '''
    Connect to the database
    '''
    if conn_str is None:
        conn_str = '/var/cache/cauthon/cache.sqlite'
    conn = sqlite3.connect(conn_str, **kwargs)
    conn.text_factory = str
    _init_db(conn, table, schema)
    return conn


def _init_db(conn, table='sites', schema=None):
    '''
    Ensure that the database is initialized
    '''
    try:
        conn.execute('SELECT COUNT(*) FROM {0}'.format(table))
    except OperationalError:
        if schema is None:
            schema = '''CREATE TABLE sites (
                url text,
                content blob,
                title text,
                last text
            )'''
        conn.execute(schema)


def insert(conn, table, *args):
    '''
    Insert data into the database
    '''
    valstr = '?,' * len(args)
    valstr = valstr.rstrip(',')
    conn.execute('INSERT INTO {0} VALUES ({1})'.format(table, valstr), args)
    conn.commit()

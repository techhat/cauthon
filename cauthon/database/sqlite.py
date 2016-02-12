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


def connect(conn_str=None, **kwargs):
    '''
    Connect to the database
    '''
    if conn_str is None:
        conn_str = '/var/cache/cauthon/cache.sqlite'
    conn = sqlite3.connect(conn_str, **kwargs)
    conn.text_factory = str
    _init_db(conn)
    return conn


def _init_db(conn):
    '''
    Ensure that the database is initialized
    '''
    try:
        conn.execute('SELECT COUNT(*) FROM sites')
    except OperationalError:
        conn.execute('''CREATE TABLE sites (
            url text,
            content blob,
            title text,
            last text
        )''')


def insert(conn, table, *args):
    '''
    Insert data into the database
    '''
    valstr = '?,' * len(args)
    valstr = valstr.rstrip(',')
    conn.execute('INSERT INTO {0} VALUES ({1})'.format(table, valstr), args)
    conn.commit()

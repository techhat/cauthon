# -*- coding: utf-8 -*-
'''
Cauthon Config
'''
import os.path
import yaml
import salt.syspaths
import salt.config

DEFAULT_OPTS = {}


def load_config(path):
    '''
    Read in the cauthon config and return the dict
    '''
    overrides = salt.config.load_config(
        path,
        'CAUTHON_CONFIG',
        os.path.join(salt.syspaths.CONFIG_DIR, 'cauthon')
    )
    config = DEFAULT_OPTS.copy()
    config.update(overrides)
    return config


def load_config_name(opts, name):
    '''
    Load a specific type of config
    '''
    conf_files = []
    config = {}
    econf = os.path.join(
        salt.syspaths.CONFIG_DIR,
        opts.get('{0}_file'.format(name), 'cauthon.{0}'.format(name))
    )
    if os.path.isfile(econf):
        conf_files.append(econf)

    ddir = os.path.join(
        salt.syspaths.CONFIG_DIR,
        opts.get('{0}_dir'.format(name), 'cauthon.{0}.d'.format(name))
    )
    for item in os.listdir(ddir):
        if item.endswith('.conf'):
            conf_files.append(os.path.join(ddir, item))

    for filename in conf_files:
        with salt.utils.fopen(filename) as fn_:
            data = yaml.safe_load(fn_.read())
        config.update(data)

    return config

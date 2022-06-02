#!/usr/bin/env python
import configparser
import os

env = os.getenv('DBENV', 'local')

# Absolute path to the directory this file is in
config_dir = os.path.dirname(__file__)
Config = configparser.ConfigParser()
print(config_dir, env)
Config.read(os.path.join(config_dir, env, 'config.ini'))


class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)


def read_config():
    cfg = configparser.ConfigParser(interpolation=EnvInterpolation())
    root = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(root, env, 'config.ini')
    if os.path.isfile(config_file):
        cfg.read(config_file)
        return cfg
    else:
        return ''


def get_database():
    cfg = read_config()
    name = 'aws'
    if name in cfg:
        cfg = cfg[name]
        return cfg
    else:
        raise Exception("There is no " + name + " configuration available...")


def get_url_services():
    cfg = read_config()
    name = 'url-services'
    if name in cfg:
        cfg = cfg[name]
        return cfg
    else:
        raise Exception("There is no " + name + " configuration available...")


def get_redis():
    cfg = read_config()
    name = 'redis'
    if name in cfg:
        cfg = cfg[name]
        return cfg
    else:
        raise Exception("There is no " + name + " configuration available...")

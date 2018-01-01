#coding=utf8

'''config file'''

class config(object):
    '''basic config'''

    URL_FORMAT = 'http://{host}:{port}/{endpoint}'
    HOST = '127.0.0.1'
    PORT = '5000'

    # endpoint
    ENDPOINT = {
        'upload': 'message',
        'ping': 'ping',
        'user': 'user'
    }

class debug_config(config):
    HOST = '127.0.0.1'
    # HOST = '192.168.0.104'
    PORT = '5000'

class product_config(config):
    HOST = '116.196.113.214'
    PORT = '5000'

class user_config(config):
    PORT = '5002'

ENV = {
    'TEST': debug_config,
    'PRODUCT': product_config,
    'USER': user_config,
    'DEFAULT_ENV': debug_config
}

REDIS_CONF = {
    'host': '127.0.0.1',
    'port': '6379',
}

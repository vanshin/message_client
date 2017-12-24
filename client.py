#coding=utf8

''' client '''

import os
import click


from requests import post, get

class config:
    test = {
        'host': '127.0.0.1',
        'port': '5000',
    }
    server = {
        'host': '116.196.113.214',
        'port': '5000',
    }
    endpoint = {
        'upload': 'message',
        'check': 'ping'
    }
    env = {
        'test': test,
        'server': server,
        'url_format': 'http://{host}:{port}/{endpoint}'
    }

def format_url(host, port, endpoint, format_str=config.env['url_format']):
    url = format_str.format(
        host = host,
        port = port,
        endpoint = endpoint
    )
    return url


def get_url(location ,endpoint):
    env_test = config.env['test']
    host=env_test['host'],
    port=env_test['port'],
    endpoint=config.endpoint[endpoint]

    if location in config.env:
        env = config.env[location]
        host = env['host']
        port = env['port']

    url = format_url(
        host = host,
        port = port,
        endpoint = endpoint,
    )
    return url


@click.command()
@click.option('--content', type=click.STRING, help='填写消息内容', prompt='内容')
@click.option('--type', type=click.INT, help='消息类型(1-文字消息)', prompt='类型')
def upload(content, type):
    data = {
        'content': content,
        'type': type,
    }
    ret = post(get_url('test', 'upload'), data=data)
    return ret.text
@click.command()
@click.option('--condi', type=click.STRING, help='环境', prompt='环境')
def check(condi):
    print(condi)
    ret = ''
    if condi == 'check':
        ret = get(get_url('test', 'check'))
    else:
        ret = get(get_url('server', 'check'))
        print('adf')
    print(ret.text)
    return ret.text

@click.command()
@click.option('--select', type=click.STRING, help='check/upload', prompt='select')
def main(select):
    if select == 'check':
        print(check())
    elif select == 'upload':
        print(upload())

    else:
        print('not exist')


if __name__ == '__main__':
    main()

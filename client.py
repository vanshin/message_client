#coding=utf8

'''客户端'''

import os
import click

from requests import post, get

from config import ENV
from runtime import redis

def get_url(endpoint):

    env = ENV.get(redis.get('env')) or ENV['DEFAULT_ENV']

    return env.URL_FORMAT.format(host=env.HOST, port=env.PORT, endpoint=endpoint)

@click.command()
@click.option('--content', type=click.STRING, help='填写消息内容', prompt='内容')
@click.option('--type', type=click.INT, help='消息类型(1-文字消息)', prompt='类型')
def upload(content, type):
    data = {
        'content': content,
        'type': type,
    }
    ret = post(get_url('upload'), data=data)
    return ret.text

def ping():
    print(get_url('ping'))
    ret = get(get_url('ping'))
    return ret.text

@click.command()
@click.option('--select', type=click.STRING, help='check/upload', prompt='select')
def main(select):
    if select == 'ping':
        print(ping())
    elif select == 'upload':
        print(upload())
    else:
        print('not exist')


if __name__ == '__main__':
    main()

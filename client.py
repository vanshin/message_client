#!/home/vanshin/.pyenv/shims/python
#coding=utf8

''' client '''

import os
import click
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

from requests import post, get

from config import ENV
from runtime import redis

def get_url(endpoint):
    env = ENV['DEFAULT_ENV']

    if redis.get('env'):
        log.info('redis_ret={}'.format(redis.get('env').decode()))
        env = ENV[redis.get('env').decode()]

    log.info('env_ret={}'.format(
        env.HOST+':'+env.PORT+'/'+env.ENDPOINT.get(endpoint)))

    return env.URL_FORMAT.format(
        host=env.HOST,
        port=env.PORT,
        endpoint=env.ENDPOINT[endpoint]
    )

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

@click.command()
def ping():
    ret = get(get_url('ping'))
    log.info('ret={}'.format(ret.text))
    return ret.text

@click.command()
@click.option('--username', type=click.STRING, help='username?', prompt='username')
@click.option('--password', type=click.STRING, help='password?', prompt='password')
@click.option('--email', type=click.STRING, help='email?', prompt='email')
@click.option('--mobile', type=click.STRING, help='mobile?', prompt='mobile')
def regi(username, email, mobile, password):
    data = {
        'username': username,
        'email': email,
        'mobile': mobile,
        'password': password
    }
    ret = post(get_url('user'), data=data)
    log.info('ret={}'.format(ret.text))
    return ret.text

@click.command()
@click.option('--username', type=click.STRING, help='username?', prompt='username')
@click.option('--password', type=click.STRING, help='password?', prompt='password')
def login(username, password):
    data = {
        'username': username,
        'password': password
    }
    ret = post(get_url('login'), data=data)
    log.info('ret={}'.format(ret.text))
    return ret.text


@click.command()
@click.option('--env', type=click.STRING, help='select one server', prompt='env')
@click.option('--expire', type=click.INT, help='redis expire time', prompt='expire')
def server(env, expire):
    redis.set('env', env)
    redis.expire('env', expire)
    log.info('ret={}'.format(redis.get('env')))
    return redis.get('env')


@click.group()
def main():
    pass

main.add_command(ping)
main.add_command(regi)
main.add_command(server)
main.add_command(upload)
main.add_command(login)


if __name__ == '__main__':
    main()

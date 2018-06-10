#!/home/vanshin/.pyenv/shims/python
#coding=utf8

''' client '''

import os
import click
import copy
import json
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

from requests import post, get, put
from prettytable import PrettyTable

from config import ENV
from runtime import redis
from base import Base
from util import is_valid_json

def pretty_data(data, name='', title=''):
    pretty = PrettyTable()
    if title:
        pretty.get_string(title=title)
    if not name:
        pretty.header = False
    if isinstance(data, dict):
        head = [name+'_k', name+'_v']
        pretty.field_names = head
        for k,v in data.items():
            if isinstance(v, (str)):
                v = pretty_data(json.loads(v)) if is_valid_json(v) else v
            else:
                v = pretty_data(v)
            pretty.add_row([k, v])
    elif isinstance(data, (set, list)):
        pretty.field_names = [name+'_i', name+'_v']
        for k,v in enumerate(data):
            if isinstance(v, (str)):
                v = pretty_data(json.loads(v)) if is_valid_json(v) else v
            else:
                v = pretty_data(v)
            pretty.add_row([k, v])
    else:
        pretty = data
    return pretty


def kformat(data, display=None, title=''):
    if not display:
        print(pretty_data(data, title=title))
        return
    if not isinstance(display, dict):
        print('use dict for display type')
        return
    for k,v in display.items():
        tmp = {}
        for item in v:
            item_list = item.split('.')
            item_data = copy.deepcopy(data)
            for i in item_list:
                item_data = item_data.get(i, {})
            tmp[item] = item_data
        print(pretty_data(tmp, k, title=title))

def lformat(data, head):
    x = PrettyTable()
    field_names = []
    field_names = [i[0] for i in head]
    field_names.insert(0 ,'index')
    x.field_names = field_names
    for i,v in enumerate(data):
        i += 1
        tmp_list = [i]
        for h in head:
            head_disp = h[0]
            head_str = h[1]
            tmp_list.append(v.get(head_str))
        x.add_row(tmp_list)

    print(x)


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
@click.option('--content', '-c', type=click.STRING, help='填写消息内容', prompt='内容')
@click.option('--type', '-t', type=click.INT, help='消息类型(1-文字消息)', prompt='类型')
@click.option('--attr', '-a', type=(click.STRING, click.STRING), multiple=True)
@click.option('--descr', '-d', type=click.STRING, help='描述', prompt='描述信息')
def upload(content, type, descr, attr):
    data = {
        'content': content,
        'type': type,
        'descr': descr,
        'attr': ''
    }
    tmp = {}
    for item in attr:
        tmp[item[0]] = item[1]
    data['attr'] = json.dumps(tmp)
    ret = post(get_url('upload'), data=data, cookies={'session_id': redis.get('session').decode()})
    data['message'] = ret.json()['message']
    kformat(data)
    return ret.text

@click.command()
@click.option('--content', '-c', type=click.STRING, help='填写消息内容', prompt='内容')
@click.option('--attr', '-a', type=(click.STRING, click.STRING), multiple=True)
@click.option('--descr', '-d', type=click.STRING, help='描述', prompt='描述信息')
@click.option('--mid', '-m', type=click.STRING, help='描述', prompt='描述信息')
def update(content, descr, attr, mid):
    data = {
        'content': content,
        'descr': descr,
        'attr': '',
        'mid': mid,
    }
    tmp = {}
    for item in attr:
        tmp[item[0]] = item[1]
    data['attr'] = json.dumps(tmp)
    ret = put(get_url('update'), data=data, cookies={'session_id': redis.get('session').decode()})
    kformat(data)
    return ret.text

@click.command()
@click.option('--type', '-t', type=click.STRING, help='type tpye', prompt='type')
@click.option('--attr', '-a', type=(click.STRING, click.STRING), multiple=True)
def gmes(type, attr):
    data = {'type': type}
    tmp = {}
    for item in attr:
        tmp[item[0]] = item[1]
    data['attr'] = json.dumps(tmp)
    ret = get(get_url('gmes'), data=data, cookies={'session_id': redis.get('session').decode()})

    result = {}
    result['code'] = ret.json()['code']
    result['message'] = ret.json()['message']
    result.update(data)
    kformat(result, title='args and descr')

    head_list = [('类型', 'type'), ('内容', 'content'),
            ('创建时间', 'create_time'), ('ID', 'id'),
            ('状态', 'status')]
    lformat(ret.json()['data']['messages'], head_list)
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
    ret = post(get_url('regi'), data=data)
    data['message'] = ret.json()['message']
    kformat(data)
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
    sess = ret.json().get('data', {}).get('session_id')
    redis.set('session', sess)
    data['session'] = sess
    kformat(data)
    return ret.text


@click.command()
@click.option('--env', type=click.STRING, help='select one server', prompt='env')
@click.option('--expire', type=click.INT, help='redis expire time', prompt='expire')
def server(env, expire):
    redis.set('env', env)
    redis.expire('env', expire)
    data = {}
    data['env'] = redis.get('env')
    data['expire'] = expire
    kformat(data)
    return redis.get('env')


@click.group()
def main():
    pass

main.add_command(ping)
main.add_command(regi)
main.add_command(server)
main.add_command(upload)
main.add_command(login)
main.add_command(gmes)
main.add_command(update)


if __name__ == '__main__':
    main()

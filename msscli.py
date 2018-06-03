#!/home/vanshin/.pyenv/shims/python
#coding=utf8

''' client '''

import os
import click
import json
import prettytable
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

from requests import post, get

from config import ENV
from runtime import redis
from base import Base

class MesCli(click.MultiCommand):

    # @click.command()
    # @click.option('--type', '-t', type=click.STRING, help='type tpye', prompt='type')
    # @click.option('--attr', '-a', type=(click.STRING, click.STRING), multiple=True)
    def gmes(self, ctx, type, attr):
        data = {'type': type}
        tmp = {}
        for item in attr:
            tmp[item[0]] = item[1]
        data['attr'] = json.dumps(tmp)
        ret = get(get_url('gmes'), data=data)
        self.kformat(ret.json())
        return ret.text


cli = MesCli()

if __name__ == '__main__':
    cli()

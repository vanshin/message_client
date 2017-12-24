#coding=utf8

'''runtime support'''

import redis

from config import REDIS_CONF

redis = redis.Redis(REDIS_CONF['host'], REDIS_CONF['port'])

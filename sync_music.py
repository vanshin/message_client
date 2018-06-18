#coding=utf8

'''
同步网易云音乐的歌单到个人数据库
'''

import os
import sys
import json
import config
import base64
import codecs
import requests

from Crypto.Cipher import AES

from util import is_valid_json

class SyncMusic(object):

    '''为了方便持久信息'''

    def __init__(self, uid=18842680):
        self.second_params = '010001'
        self.third_params = config.THIRD_PARAM
        self.forth_params = '0CoJUm6Qyw8W8jud'
        self.uid = uid
        self.random_str = 'kfr7Iznql5c3mKZi'
        self.token = ''

    def call_163(self, ep, method='post', token='', params=None):
        if method not in ('post', 'get'):
            print('不受支持的http方法')
            return
        if isinstance(params, dict):
            params = json.dumps(params)

        data = {}
        enc = {'params': self.enc_params(params), 'encSecKey': self.get_enckey()}
        data.update(enc)
        data = config.tet_data
        token = token or self.token

        print('data={}'.format(data))

        ret = getattr(requests, method)('http://music.163.com/'+ep,
                params={'csrf_token': token}, data=data)
        print(ret)

        if not is_valid_json(ret.text):
            return ret.text
        return ret.json()

    def login(self):
        ep = 'weapi/login/cellphone'
        ret = self.call_163(ep, params=config.LOGIN)
        print(ret)

    def aes_enc(self, text, key):

        pad = 16 - len(text) % 16
        text = text + str(pad * chr(pad))
        encryptor = AES.new(key, 2, '0102030405060708')
        encrypt_text = encryptor.encrypt(text)
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    def rsa_enc(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'),'hex_codec'), 16)**int(pubKey, 16)%int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def get_enckey(self):
        ret = self.rsa_enc(self.random_str, self.second_params, self.third_params)
        return ret

    def enc_params(self, params):
        # 偏移量
        params = self.aes_enc(params, self.forth_params).decode()
        params = self.aes_enc(params, self.random_str).decode()
        return params

    def get_music_list(self):
        '''获取歌单'''
        ep = 'weapi/user/playlist'
        self.token = "46220a731630f94f44f25f586086f38d"
        params = {}
        params['csrf_token'] = self.token
        params['limit'] = "1001"
        params['offset'] = "0"
        params['uid'] = str(self.uid)
        ret = self.call_163(ep, params=params)
        print(ret)
        pass

    def get_music_of_list(self, list_id):
        ep = 'weapi/v3/playlist/detail'
        params = {}
        params['csrf_token'] = self.token
        params['limit'] = "1001"
        params['offset'] = "0"
        params['id'] = str(16340609)
        params['n'] = str(1000)
        params['total'] = True
        ret = self.call_163(ep, params=params)

        pass


    def save(self):
        pass

if __name__ == '__main__':
    sm = SyncMusic()
    sm.get_music_list()

#coding=utf8

''' 工具基础类,方法等 '''

import os
import json

from prettytable import PrettyTable

from util import is_valid_json

class Base(object):

    def _pretty_data(self, data, name='※', se='_'):
        pretty = PrettyTable()
        if isinstance(data, dict):
            head = [name+'_k', name+'_v']
            pretty.field_names = head
            for k,v in data.items():
                if isinstance(v, dict):
                    v = self._pretty_data(v)
                elif isinstance(v, (set, list)):
                    v = self._pretty_data(v)
                elif isinstance(v, (unicode, str)):
                    v = self._pretty_data(json.loads(v)) if is_valid_json(v) else v
                pretty.add_row([k, v])
        elif isinstance(data, (set, list, str)):
            pretty.field_names = [name+'_i', name+'_v']
            for k,v in enumerate(data):
                if isinstance(v, dict):
                    v = self._pretty_data(v)
                elif isinstance(v, (set, list, str)):
                    v = self._pretty_data(v)
                elif isinstance(v, (unicode, str)):
                    v = self._pretty_data(json.loads(v)) if is_valid_json(v) else v
                pretty.add_row([k, v])
        else:
            pretty = data
        return pretty


    def kformat(self, data):
        print(self._pretty_data(data))

if __name__ == '__main__':
    a = Base()
    data = {'df': 123, 'edf': 24}
    data2 = [1,2,3,4,5]
    data3 = {2,3,4,5,6}
    a.kformat(data)
    a.kformat(data2)
    a.kformat(data3)



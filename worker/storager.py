# -*- coding: utf-8 -*-
'''
Created on 2017年4月12日

@author: chenyitao
'''

import gevent
from tddc.base import StoragerBase
from tddc.common import TDDCLogging

from common.queues import ParserQueues


class ParseStorager(StoragerBase):
    '''
    classdocs
    '''
    
    FAMILY = 'valuable'
    
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(ParseStorager, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj

    def __init__(self, nodes):
        super(ParseStorager, self).__init__(nodes, True, True)

    @staticmethod
    def pull(self, task):
        ParserQueues.TASK_INPUT.put(task)

    def _pull(self):
        while True:
            task = ParserQueues.TASK_INPUT.get()
            if not task:
                continue
            if not task.platform or not task.row_key:
                TDDCLogging.error('Task Exception(Parse DB Manager): [%s:%s]' % (task.platform,
                                                                                 task.row_key))
                continue
            success, ret = self._db.get_from_hbase(task.platform,
                                                   task.row_key,
                                                   'source',
                                                   'content')
            if not success:
                ParserQueues.TASK_INPUT.put(task)
                gevent.sleep(1)
                continue
            if not ret:
                continue
            for _, value in ret.items():
                ParserQueues.WAITING_PARSE.put((task, value))
                break


def main():
    ParseStorager()
    while True:
        gevent.sleep()

if __name__ == '__main__':
    main()
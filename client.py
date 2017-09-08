# -*- coding: utf-8 -*-
'''
Created on 2017年4月14日

@author: chenyitao
'''

import gevent.monkey
gevent.monkey.patch_all()

from tddc.base import WorkerManager
from tddc.common import TDDCLogging

from parser_site import ParserSite
from worker.parser import Parser
from worker.storager import ParseStorager
from worker.task import ParseTaskManager


class ParserManager(WorkerManager):

    def __init__(self):
        TDDCLogging.info('->Parser Is Starting')
        super(ParserManager, self).__init__(ParserSite)
        self._storager = ParseStorager(ParserSite.random_hbase_node())
        self._parser = Parser()
        self._task_manager = ParseTaskManager()
        TDDCLogging.info('->Parser Was Ready.')
    
    @staticmethod
    def start():
        ParserManager()
        while True:
            gevent.sleep(15)


def main():
    ParserManager.start()

if __name__ == '__main__':
    main()

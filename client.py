# -*- coding: utf-8 -*-
'''
Created on 2017年4月14日

@author: chenyitao
'''

import gevent.monkey 
gevent.monkey.patch_all()
import os
if os.path.exists('./worker.log'):
    os.remove('./worker.log')

from tddc.base import WorkerManager, PackagesManager, EventCenter
from tddc.common import TDDCLogging

from parser_site import ParserSite
from worker.parser import Parser
from worker.storager import ParseStorager
from worker.task import ParseTaskManager
from worker.common.event import TDDCEventType


class ParserManager(WorkerManager):

    def __init__(self):
        TDDCLogging.info('->Parser Is Starting')
        super(ParserManager, self).__init__(ParserSite)
        EventCenter().register(TDDCEventType.Parser.MODULES_UPDATE,
                               PackagesManager()._models_update_event)
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

# -*- coding: utf-8 -*-
'''
Created on 2017年4月14日

@author: chenyitao
'''

import os
import gevent.monkey
import setproctitle
gevent.monkey.patch_all()


from tddc import WorkerManager, Storager

from config import ConfigCenterExtern
from worker.task import TaskManager

from worker.parser import Parser
# from worker.storager import ParseStorager
# from worker.task import ParseTaskManager
# from worker.common.event import TDDCEventType


class ParserManager(WorkerManager):

    def __init__(self):
        super(ParserManager, self).__init__()
        self.info('Parser Is Starting')
        Storager()
        TaskManager()
        # EventCenter().register(TDDCEventType.Parser.MODULES_UPDATE,
        #                        PackagesManager()._models_update_event)
        # self._storager = ParseStorager(ParserSite.random_hbase_node())
        Parser()
        # self._task_manager = ParseTaskManager()
        self.info('Parser Was Ready.')
    
    @staticmethod
    def start():
        if os.path.exists('./worker.log'):
            os.remove('./worker.log')
        ConfigCenterExtern()
        setproctitle.setproctitle(ConfigCenterExtern().get_worker().name)
        ParserManager()
        while True:
            gevent.sleep(15)


def main():
    ParserManager.start()


if __name__ == '__main__':
    main()

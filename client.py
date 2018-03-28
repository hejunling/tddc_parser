# -*- coding: utf-8 -*-
'''
Created on 2017年4月14日

@author: chenyitao
'''
import logging
import os
import gevent.monkey
import setproctitle

gevent.monkey.patch_all()

from tddc import WorkerManager, TaskManager, WorkerModel, DBSession

from worker.parser import Parser

logging.getLogger('PIL').setLevel(logging.WARN)
log = logging.getLogger(__name__)


class ParserManager(WorkerManager):

    def __init__(self):
        log.info('Parser Is Starting')
        super(ParserManager, self).__init__()
        TaskManager()
        Parser()
        log.info('Parser Was Ready.')
    
    @staticmethod
    def start():
        if os.path.exists('./worker.log'):
            os.remove('./worker.log')
        setproctitle.setproctitle(DBSession.query(WorkerModel).get(1).platform)
        ParserManager()
        while True:
            gevent.sleep(15)


def main():
    ParserManager.start()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
'''
Created on 2017年4月11日

@author: chenyitao
'''

import gevent
from tddc.base import PackagesManager
from tddc.common import TDDCLogging
from tddc.common.models.task import Task

from worker.common.queues import ParserQueues


class Parser(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        TDDCLogging.info('-->Parser Is Starting.')
        gevent.spawn(self._parse)
        gevent.sleep()
        TDDCLogging.info('-->Parser Was Ready.')

    def _parse(self):
        while True:
            task, body = ParserQueues.WAITING_PARSE.get()
            cls = PackagesManager().get_parse_model(task.platform, task.feature)
            if not cls:
                fmt = 'Parse No Match: [P:{platform}][F:{feature}][K:{row_key}]'
                TDDCLogging.warning(fmt.format(platform=task.platform,
                                               feature=task.feature,
                                               row_key=task.row_key))
                ParserQueues.TASK_STATUS.put((task,
                                              Task.Status.PARSE_FAILED,
                                              Task.Status.WAIT_PARSE))
                continue
            try:
                ret = cls(task, body)
            except Exception, e:
                TDDCLogging.error(e)
                ParserQueues.TASK_STATUS.put((task,
                                              Task.Status.PARSE_FAILED,
                                              Task.Status.WAIT_PARSE))
                continue
            self._storage(task, ret.items)
            self._new_task_push(ret.tasks)
            fmt = 'Parsed: [{platform}:{row_key}:{feature}][S:{items}][N:{tasks}]'
            TDDCLogging.info(fmt.format(platform=task.platform,
                                        feature=task.feature,
                                        row_key=task.row_key,
                                        items=len(ret.items),
                                        tasks=len(ret.tasks)))
            ParserQueues.TASK_STATUS.put((task,
                                          Task.Status.PARSE_SUCCESS,
                                          Task.Status.WAIT_PARSE))

    @staticmethod
    def _storage(task, items):
        if len(items):
            ParserQueues.STORAGE.put([task, items])

    @staticmethod
    def _new_task_push(tasks):
        for task in tasks:
            ParserQueues.TASK_OUTPUT.put(task)

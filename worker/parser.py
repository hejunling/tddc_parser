# -*- coding: utf-8 -*-
'''
Created on 2017年4月11日

@author: chenyitao
'''

import gevent
from tddc import TDDCLogger, ExternManager, HBaseManager, Storager

from worker.task import TaskManager, TaskStatus


class Parser(TDDCLogger):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(Parser, self).__init__()
        self.info('Parser Is Starting.')
        gevent.spawn(self._parse)
        gevent.sleep()
        self.info('Parser Was Ready.')

    def _parse(self):
        while True:
            task = TaskManager().get()
            cls = ExternManager().get_model(task.platform, task.feature)
            if not cls:
                task.cur_status, task.pre_status = TaskStatus.ParseModuleNotFound, task.cur_status
                TaskManager().task_failed(task)
                continue
            HBaseManager().get_async(self._parsing,
                                     task.platform,
                                     task.row_key,
                                     'source',
                                     'content',
                                     task=task,
                                     cls=cls)

    def _parsing(self, data, task, cls):
        ret = None
        try:
            if len(data) == 2 and data[0] and data[1]:
                ret = cls(task, data[1].values()[0])
            else:
                self.warning('[%s:%s:%s] Fetched Data Error.' % (task.platform,
                                                                 task.id,
                                                                 task.url))
                task.cur_status, task.pre_status = TaskStatus.ParsedFailed, task.cur_status
                TaskManager().task_failed(task)
                return
        except Exception as e:
            self.exception(e)
            task.cur_status, task.pre_status = TaskStatus.ParsedFailed, task.cur_status
            TaskManager().task_failed(task)
            return
        self._storage(task, ret.items)
        self._push_new_task(task, ret.tasks)
        task.cur_status, task.pre_status = TaskStatus.ParsedSuccess, task.cur_status
        TaskManager().task_successed(task,
                                     None)

    def _storage(self, task, items):
        if not len(items):
            return

    def _push_new_task(self, task, tasks):
        if not len(tasks):
            return
        for new_task in tasks:
            TaskManager().push_task(new_task,
                                    'tddc_crawl')
        self.debug('[%s:%s] Generate %d New Task.' % (task.platform,
                                                      task.id,
                                                      len(tasks)))

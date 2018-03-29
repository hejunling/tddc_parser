# -*- coding: utf-8 -*-
'''
Created on 2017年4月11日

@author: chenyitao
'''
import logging

import gevent
from tddc import ExternManager, Storager, TaskManager, Task, TaskCacheManager, TaskRecordManager

log = logging.getLogger(__name__)


class Parser(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        log.info('Parser Is Starting.')
        self.task_conf = TaskManager().task_conf
        super(Parser, self).__init__()
        gevent.spawn(self._parse)
        gevent.sleep()
        log.info('Parser Was Ready.')

    def _parse(self):
        while True:
            task = TaskManager().get()
            cls = ExternManager().get_model(task.platform, task.feature)
            if not cls:
                task.status = Task.Status.ParseModuleNotFound
                TaskManager().task_failed(task)
                continue
            conetnt = TaskCacheManager().get_cache(task)
            self._parsing(conetnt, task, cls)

    def _parsing(self, data, task, cls):
        try:
            if data and len(data):
                ret = cls(task, data)
            else:
                log.warning('[%s:%s:%s] Fetched Data Error.' % (task.platform,
                                                                task.id,
                                                                task.url))
                task.status = Task.Status.ParsedFailed
                TaskManager().task_failed(task)
                return
        except Exception as e:
            log.exception(e)
            task.status = Task.Status.ParsedFailed
            TaskManager().task_failed(task)
            return
        if ret.items:
            Storager().storage_to_mongo(ret.db, ret.table, ret.items)
        if ret.tasks:
            self._push_new_task(task, ret.tasks)
        task.status = Task.Status.ParsedSuccess
        TaskManager().task_successed(task)

    def _push_new_task(self, task, tasks):
        if not len(tasks):
            return
        for new_task in tasks:
            TaskRecordManager().create_record(new_task)
            TaskManager().push_task(new_task, self.task_conf.crawler_topic)
        log.debug('[%s:%s] Generate %d New Task.' % (task.platform,
                                                     task.id,
                                                     len(tasks)))

# -*- coding: utf-8 -*-
'''
Created on 2017年4月11日

@author: chenyitao
'''

import gevent
import time
from tddc import TDDCLogger, ExternManager, Storager, TaskManager, TaskStatus, RecordManager, object2json, StatusManager

from config import ConfigCenterExtern


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
            Storager().get_async(self._parsing,
                                 task.platform,
                                 task.id,
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
        if ret.items:
            Storager().storage(ret.items)
        if ret.tasks:
            self._push_new_task(task, ret.tasks)
        task.cur_status, task.pre_status = TaskStatus.ParsedSuccess, task.cur_status
        TaskManager().task_successed(task)

    def _push_new_task(self, task, tasks):
        task_conf = ConfigCenterExtern().get_task()
        if len(tasks):
            name = '%s:%s' % (ConfigCenterExtern().get_task().record_key_base,
                              task.platform)
            records = {record.id: object2json(record) for record in tasks}
            RecordManager().create_records(name, records)
            cur_time = time.time()
            name = '%s:%s:%d' % (task_conf.status_key_base,
                                 task.platform,
                                 TaskStatus.CrawlTopic)
            status = {record.id: cur_time for record in tasks}
            StatusManager().set_multi_status(name, status)
        for new_task in tasks:
            TaskManager().push_task(new_task, task_conf.producer_topic, False)
        self.debug('[%s:%s] Generate %d New Task.' % (task.platform,
                                                      task.id,
                                                      len(tasks)))

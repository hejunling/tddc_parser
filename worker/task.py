# -*- coding: utf-8 -*-
'''
Created on 2017年4月12日

@author: chenyitao
'''

from tddc.base import BloomFilter, TaskManagerBase
from tddc.common import TDDCLogging
from tddc.common.models import Task

from parser_site import ParserSite
from worker.common.queues import ParserQueues


class ParseTaskManager(TaskManagerBase):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        TDDCLogging.info('-->Task Manager Is Starting.')
        super(ParseTaskManager, self).__init__(ParserSite, ParserQueues)
        self._filter = BloomFilter()
        TDDCLogging.info('-->Task Manager Was Ready.')

    def task_status_process(self, task):
        self.update_status(task,
                           Task.Status.WAIT_PARSE,
                           Task.Status.CRAWL_SUCCESS)

    def ready_to_push(self, task):
#         if not self._filter.setget(task.url):
#             TDDCLogging.debug('New Task [%s:%s] Was Filter.' % (task.platform, task.url))
#             return False
#         self.create_record(task)
        return True

    def pushed(self, task):
        self.update_status(task,
                           Task.Status.CRAWL_TOPIC,
                           None)
    

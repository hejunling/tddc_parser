# -*- coding: utf-8 -*-
'''
Created on 2017年4月13日

@author: chenyitao
'''

from tddc import Task
from ..parse_rule_base import ParseRuleBase


class Che300DetailPage(ParseRuleBase):
    '''
    classdocs
    '''

    platform = 'che300'

    feature = 'che300.deatil'

    version = '1495799988'

    def _parse(self):
        self._make_pinggu_task()

    def _make_pinggu_task(self):
        pinggu_url = self._xpath('//*[@class="dtir-cp"]/p[2]/a/@href')
        task = Task()
        task.status = Task.Status.CrawlTopic
        task.url = pinggu_url.extract()[0].replace('https', 'http')
        task.platform = self.platform
        task.feature = 'che300.pinggu'
        task.headers = {'Referer': self._task.url,
                        'Set-Cookie': self._task.headers.get('Set-Cookie')}
        self.tasks.append(task)

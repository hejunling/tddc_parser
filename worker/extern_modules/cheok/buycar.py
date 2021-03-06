# -*- coding: utf-8 -*-
'''
Created on 2017年4月13日

@author: chenyitao
'''


from tddc import ShortUUID, Task

from ..parse_rule_base import ParseRuleBase


class CheokBuyCar(ParseRuleBase):
    '''
    classdocs
    '''

    platform = 'cheok'

    feature = 'cheok.buycar'

    version = '14957789222'

    valid = '1'

    test = 'xxxxxxxxx'

    def _parse(self):
        self._car_list_pages_task()
        self._detail_task()
        # self.tasks = self.tasks[60:80]

    def _car_list_pages_task(self):
        cur_page = self._xpath('//*[@class="num curr"]/text()')
        cur_page = cur_page[0] if len(cur_page) else None
        if cur_page != '1':
            return
        page_numbers = self._xpath('//*[@class="num"][last()]/text()')
        page_numbers = int(page_numbers[0]) if len(page_numbers) else None
        if not page_numbers:
            return
        base_url = 'http://www.cheok.com/buycar/b_0_st_0_cp_%d_pg_20/'
        for page_number in range(2, page_numbers + 1):
            url = base_url % page_number
            task = Task()
            task.url = url
            task.platform = self.platform
            task.feature = self.feature
            task.referer = self._task.url
            task.status = Task.Status.CrawlTopic
            task.proxy = 'HTTP'
            self.tasks.append(task)

    def _detail_task(self):
        detail_urls = self._xpath('//*[@class="car-item"]/@href')
        for url in detail_urls:
            url = 'http://www.cheok.com%s' % url
            task = Task()
            task.url = url
            task.platform = self.platform
            task.feature = 'cheok.car_detail'
            task.referer = self._task.url
            task.status = Task.Status.CrawlTopic
            task.proxy = 'HTTP'
            self.tasks.append(task)

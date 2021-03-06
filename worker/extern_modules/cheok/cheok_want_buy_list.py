# -*- coding: utf-8 -*-
'''
Created on 2017年4月18日

@author: chenyitao
'''
from tddc import Task
from ..parse_rule_base import ParseRuleBase


class CheokWantBuyList(ParseRuleBase):
    '''
    classdocs
    '''

    platform = 'cheok'

    feature = 'cheok.want_buy_list'
    
    version = '1495799977'

    def _parse(self):
        if self._body_type != self.JSON:
            print('(%s)Error. Not JSON.' % self.__class__)
            return
        self._want_buy_list()

    def _want_buy_list(self):
        if self._json_dict.get('code') != 1:
            print('(%s)Error. Response Code:%d.' % (self.__class__, self._json_dict.get('code', -1000)))
            return
        objs = self._json_dict.get('object')
        if objs and len(objs):
            base_url = 'http://www.cheok.com/{cityAcronym}/sn/{carSourceNo}.html'
            for info in objs:
                url = base_url.format(cityAcronym=info.get('cityAcronym'),
                                      carSourceNo=info.get('carSourceNo'))
                task = Task()
                task.status = Task.Status.CrawlTopic
                task.url = url
                task.platform = self.platform
                task.feature = 'cheok.want_buy_detail'
                task.cookie = 'JSESSIONID=3A32AF91FE59B1F06A61954C280DFC12'
                task.headers = {'Referer': ('http://www.cheok.com/car/cp_' 
                                            + str(self._json_dict.get('page').get('currentPage')))}
                self._md5_mk.update(url)
                task.row_key = self._md5_mk.hexdigest()
                self.tasks.append(task)

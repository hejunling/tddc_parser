# -*- coding: utf-8 -*-
"""
Created on 2017年8月31日

@author: chenyitao
"""

from tddc import ConfigCenter


class ConfigCenterExtern(ConfigCenter):

    @staticmethod
    def tables():
        return dict(ConfigCenter.tables(),
                    **{'task': {'consumer_topic': 'TEXT',
                                'consumer_group': 'TEXT',
                                'producer_topic': 'TEXT',
                                'status_key_base': 'TEXT',
                                'record_key_base': 'TEXT',
                                'local_task_queue_size': 'TEXT'}})

    def get_task(self):
        return self._get_info('task')

# -*- coding: utf-8 -*-
'''
Created on 2017年6月20日

@author: chenyitao
'''

from tddc.base import PackagesManager
from worker import EventType


class ParsePackagesManager(PackagesManager):
    '''
    classdocs
    '''

    EVENT_TYPE = EventType.Parser.MODULE
    
    CONF_PATH = './conf/parse_rule_index/'
    
    PACKAGE_PATH = './worker/worker/parser_moulds/'

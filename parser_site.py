# -*- coding: utf-8 -*-
'''
Created on 2017年6月15日

@author: chenyitao
'''

from tddc import conf

from worker.common import event
from worker.common.event import EventType


class ParserSite(conf.SiteBase):
 
    # Parse Rules HBase Table Info
    RULES_TABLE = 'tddc_p_rules'
    RULES_FAMILY = 'rules'
    RULES_QUALIFIER = 'index'
    
    # Parse Event Topic Info
    EVENT_TOPIC = 'tddc_p_event'

    # Task Input Topic Info
    TASK_INPUT_TOPIC = 'tddc_parse'
    TASK_INPUT_TOPIC_GROUP = 'tddc.p.parser'

    # Task Output Topic Info
    TASK_OUTPUT_TOPIC = 'tddc_crawl'
    
    # Parser Concurrent
    FETCH_SOURCE_CONCURRENT = 8

    EVENT_TABLES = {EventType.Parser.BASE_DATA: event.ParserBaseDataEvent,
                    EventType.Parser.MODULE: event.ParseModuleEvent}
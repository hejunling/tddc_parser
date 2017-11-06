# -*- coding: utf-8 -*-
'''
Created on 2017年6月15日

@author: chenyitao
'''

from tddc import conf

from worker.common import event


class ParserSite(conf.SiteBase):

    # Parse Rules HBase Table Info
    RULES_TABLE = 'tddc_p_rules'
    RULES_FAMILY = 'rules'
    RULES_QUALIFIER = 'index'
    
    # Parse Event Topic Info
    EVENT_TOPIC = 'tddc_event_parser'

    # Task Input Topic Info
    TASK_INPUT_TOPIC = 'tddc_parse'
    TASK_INPUT_TOPIC_GROUP = 'tddc.p.parser'

    # Task Output Topic Info
    TASK_OUTPUT_TOPIC = 'tddc_crawl'
    
    # Parser Concurrent
    FETCH_SOURCE_CONCURRENT = 8

    EVENT_TABLES = {event.TDDCEventType.Parser.MODULES_UPDATE: event.TDDCEvent.Parser.ModulesUpdate}

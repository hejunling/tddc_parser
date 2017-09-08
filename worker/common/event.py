# -*- coding: utf-8 -*-
'''
Created on 2017年9月6日

@author: chenyitao
'''

from tddc.common.models.events_model.event_base import EventBase


class EventType(object):

    NONE = None

    class Parser(object):
        
        BASE_DATA = 2001
    
        MODULE = 2002


class ParseModuleEvent(EventBase):

    event_type = EventType.Parser.MODULE


class ParserBaseDataEvent(EventBase):

    event_type = EventType.Parser.BASE_DATA

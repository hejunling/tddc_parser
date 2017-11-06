# -*- coding: utf-8 -*-
'''
Created on 2017年9月6日

@author: chenyitao
'''

from tddc.common.models.events_model.event_base import EventBase
from tddc.common.models.model_base import QuickModelBase


class TDDCEventType(object):

    class Crawler(object):

        MODULES_UPDATE = 1001

    class Parser(object):

        MODULES_UPDATE = 2001

    class ProxyChecker(object):

        MODULES_UPDATE = 3001

    class Monitor(object):

        MODULES_UPDATE = 4001

    class CookiesGenerator(object):

        MODULES_UPDATE = 5001


class TDDCEvent(object):

    class _ModulesUpdateEvent(QuickModelBase):

        @staticmethod
        def members():
            return dict(QuickModelBase.members(),
                        **{'platform': None,
                           'table': None})

    class Crawler(object):

        class ModulesUpdate(EventBase):

            EVENT_TYPE = TDDCEventType.Crawler.MODULES_UPDATE

            @staticmethod
            def members():
                return dict(EventBase.members(),
                            **{'name': 'Crawler.ModulesUpdate'})

            @staticmethod
            def types():
                return dict(EventBase.types(),
                            **{'event': TDDCEvent._ModulesUpdateEvent})

    class Parser(object):

        class ModulesUpdate(EventBase):

            EVENT_TYPE = TDDCEventType.Parser.MODULES_UPDATE

            @staticmethod
            def types():
                return dict(EventBase.types(),
                            **{'event': TDDCEvent._ModulesUpdateEvent})

    class ProxyChecker(object):

        class ModulesUpdate(EventBase):

            EVENT_TYPE = TDDCEventType.ProxyChecker.MODULES_UPDATE

            @staticmethod
            def types():
                return dict(EventBase.types(),
                            **{'event': TDDCEvent._ModulesUpdateEvent})

    class Monitor(object):

        class ModulesUpdate(EventBase):

            EVENT_TYPE = TDDCEventType.Monitor.MODULES_UPDATE

            @staticmethod
            def types():
                return dict(EventBase.types(),
                            **{'event': TDDCEvent._ModulesUpdateEvent})

    class CookiesGenerator(object):

        class ModulesUpdate(EventBase):

            EVENT_TYPE = TDDCEventType.CookiesGenerator.MODULES_UPDATE

            @staticmethod
            def types():
                return dict(EventBase.types(),
                            **{'event': TDDCEvent._ModulesUpdateEvent})

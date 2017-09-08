# -*- coding: utf-8 -*-
'''
Created on 2017年9月6日

@author: chenyitao
'''

from gevent.queue import Queue
from tddc.common.queues import PublicQueues


class ParserQueues(PublicQueues):
    ## Parser
    # Parser Rules Moulds Update Queue
    PARSER_RULES_MOULDS_UPDATE = Queue()
    # Waiting For Parse Queue
    WAITING_PARSE = Queue()
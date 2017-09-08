# -*- coding: utf-8 -*-
'''
Created on 2017年9月7日

@author: chenyitao
'''

from tddc.common.models.exception.base import ExceptionModelBase


class ExceptionType(object):

    class Parser(object):
        CLIENT = 2101
        TASK_FAILED = 2201
        TASK_NO_PARSE_MODEL = 2202
        STORAGE_FAILED = 2301
        STORAGER_EXCEPTION = 2302


class ParserClientException(ExceptionModelBase):

    EXCEPTION_TYPE = ExceptionType.Parser.CLIENT


class ParserTaskFailedException(ExceptionModelBase):

    EXCEPTION_TYPE = ExceptionType.Parser.TASK_FAILED


class ParserTaskNoParseModelException(ExceptionModelBase):

    EXCEPTION_TYPE = ExceptionType.Parser.TASK_NO_PARSE_MODEL


class ParserSrorageFailedException(ExceptionModelBase):

    EXCEPTION_TYPE = ExceptionType.Parser.STORAGE_FAILED


class ParserStoragerException(ExceptionModelBase):

    EXCEPTION_TYPE = ExceptionType.Parser.STORAGER_EXCEPTION

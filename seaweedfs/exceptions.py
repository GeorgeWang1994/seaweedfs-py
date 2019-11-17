#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author:    george wang
@datetime:  2019-11-17
@file:      exception.py
@contact:   georgewang1994@163.com
@desc:      exception of seaweedfs
"""


class SeaweedfsError(Exception):
    pass


class JSONDecodeError(SeaweedfsError):
    pass


class PostError(SeaweedfsError):
    pass


class ParamNoneError(SeaweedfsError):
    pass

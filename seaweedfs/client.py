#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author:    george wang
@datetime:  2019-11-16
@file:      client.py
@contact:   georgewang1994@163.com
@desc:      client for seaweedfs
"""
import os
from urllib.parse import urljoin

import requests

from seaweedfs.exceptions import *


class Filer(object):
    HTTP_PREFIX = "http"
    HTTPS_PREFIX = "https"

    def __init__(self, host="localhost", port=8888, ssl=False):
        """
        :param host:
        :param port:
        :param ssl:
        """
        self.host = host
        self.port = port
        if not ssl:
            self.url = "%s://%s:%s" % (self.HTTP_PREFIX, self.host, str(self.port))
        else:
            self.url = "%s://%s:%s" % (self.HTTPS_PREFIX, self.host, str(self.port))

    def ping(self):
        """
        查看是否连接
        :return:
        """
        resp = requests.get(self.url)
        return resp.ok

    @staticmethod
    def add_slash_if_needed(url):
        """
        添加/
        :param url:
        :return:
        """
        if not url.endswith("/"):
            return url + "/"
        return url

    def upload(self, fp, filename, path):
        """
        上传文件
        :param fp: 文件句柄或者文件路径
        :param filename:
        :param path:
        :return:
        """
        if not filename or not path:
            raise ParamNoneError
        url = urljoin(self.url, self.add_slash_if_needed(path) + filename)
        _fp = open(fp, "r") if isinstance(fp, str) else fp
        try:
            resp = requests.post(url, files={"file": _fp})
            if not resp.ok:
                return False
            return True
        except PostError as e:
            raise e

    def download(self, filename, path):
        """
        下载文件
        :param filename:
        :param path:
        :return:
        """
        if not filename or not path:
            raise ParamNoneError
        url = urljoin(self.url, self.add_slash_if_needed(path) + filename)
        resp = requests.get(url)
        if not resp.ok:
            return False, None
        return True, {
            "content_length": resp.headers.get("content-length"), "content_type": resp.headers.get("content-type"),
            "content": str(resp.content, encoding="utf-8"),
        }

    def mkdir(self, path, filename=".info"):
        """
        创建目录（默认将指定文件上传）
        :param path:
        :param filename:
        :return:
        """
        if not filename and not path:
            raise ParamNoneError
        default_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), ".info")
        with open(default_path, "r") as fp:
            return self.upload(fp, filename, path)

    def list(self, path, json=False):
        """
        列表目录下的文件
        :param path:
        :param json:
        :return:
        """
        if not path:
            raise ParamNoneError
        sub_url = self.add_slash_if_needed(path) + ("?pretty=True" if json else "")
        url = urljoin(self.url, sub_url)
        headers = {'Accept': 'application/json'}
        try:
            resp = requests.get(url, headers=headers)
            return resp.json()
        except JSONDecodeError as e:
            raise e

    def exist(self, filename, path):
        """
        查找是否存在文件
        :param filename:
        :param path:
        :return:
        """
        if not filename and not path:
            raise ParamNoneError
        return self.download(filename, path)

    def delete(self, filename, path):
        """
        删除文件或者目录
        :param filename:
        :param path:
        :return:
        """
        if not filename and not path:
            raise ParamNoneError
        url = urljoin(self.url, self.add_slash_if_needed(path) + filename)
        resp = requests.delete(url)
        if not resp.ok:
            return False
        return True

#!/usr/bin/env python
# ** -- coding: utf-8 -- **

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
        添加 /
        :param url:
        :return:
        """
        url = Filer.delete_slash_if_needed(url)
        return url + "/"

    @staticmethod
    def delete_slash_if_needed(url):
        """
        清除 /
        :param url:
        :return:
        """
        return url.strip("/")

    def upload(self, fp, filename, path, raise_error=False):
        """
        上传文件
        :param fp: 文件句柄或者文件路径
        :param filename:
        :param path: 如果为根目录填 /，其余目录填 downloads/test/
        :param raise_error:
        :return: {'name': '.info', 'fid': '2,0197f5c95e53', 'url': 'http://localhost:8081/2,0197f5c95e53'}
        """
        if not filename or not path:
            raise ParamNoneError
        url = urljoin(self.url, self.add_slash_if_needed(path) + filename)
        _fp = open(fp, "rb") if isinstance(fp, str) else fp
        try:
            resp = requests.post(url, files={"file": _fp})
            if resp.ok:
                return resp.json()
            return {}
        except UploadError as e:
            if raise_error:
                raise e
            return {}

    def download(self, filename, path):
        """
        下载文件
        :param filename:
        :param path: 如果为根目录填 /，其余目录填 downloads/test/
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
            "content": resp.content,
        }

    def mkdir(self, path, filename=".info"):
        """
        创建目录（默认将指定文件上传）
        :param path: 如果为根目录填 /，其余目录填 downloads/test/
        :param filename:
        :return:
        """
        if not filename and not path:
            raise ParamNoneError
        default_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), ".info")
        with open(default_path, "r") as fp:
            return self.upload(fp, filename, path)

    def list(self, path="", last_file_name="", limit=None, raise_error=False):
        """
        列表目录下的文件
        :param path: 如果为根目录填 /，其余目录填 downloads/test/
        :param last_file_name:
        :param limit:
        :param raise_error:
        :return:
        {
            'Path': '/test',
            'Entries': [
                {
                    'FullPath': '/test/test.js',
                    'Mtime': '2019-11-18T07:33:46Z',
                    'Crtime': '2019-11-18T07:33:46Z',
                    'Mode': 432,
                    'Uid': 0,
                    'Gid': 0,
                    'Mime': 'application/javascript',
                    'Replication': '000',
                    'Collection': '',
                    'TtlSec': 0,
                    'UserName': '',
                    'GroupNames': None,
                    'SymlinkTarget': '',
                    'chunks': [{'file_id': '3,017f5aedd46f', 'size': 4, 'mtime': 1574062426611004083, 'e_tag': '"de2d6af6"', 'fid': {'volume_id': 3, 'file_key': 383, 'cookie': 1525535855}}]
                }
            ],
            'Limit': 1,
            'LastFileName': 'test.js',
            'ShouldDisplayLoadMore': True
        }
        """
        if not path:
            raise ParamNoneError

        params = []
        if last_file_name is not None:
            params.append("lastFileName=%s" % last_file_name)
        if limit is not None:
            params.append("limit=%s" % limit)

        sub_url = "%s?%s" % (self.add_slash_if_needed(path), "&".join(params))
        url = urljoin(self.url, sub_url)
        headers = {'Accept': 'application/json'}
        try:
            resp = requests.get(url, headers=headers)
            if resp.ok:
                return resp.json()
            return {}
        except JSONDecodeError as e:
            if raise_error:
                raise e
            return {}

    def exist(self, filename, path):
        """
        查找是否存在文件
        :param filename:
        :param path: 如果为根目录填 /，其余目录填 downloads/test/
        :return:
        """
        if not filename and not path:
            raise ParamNoneError
        return self.download(filename, path)[0]

    def delete(self, filename, path):
        """
        删除文件
        :param filename:
        :param path: 如果为根目录填 /，其余目录填 downloads/test/
        :return:
        """
        if not filename and not path:
            raise ParamNoneError
        url = urljoin(self.url, self.add_slash_if_needed(path) + filename)
        resp = requests.delete(url)
        if not resp.ok:
            return False
        return True

    def delete_folder(self, path):
        """
        删除目录
        :param path: 如果为根目录填 /，其余目录填 downloads/test/
        :return:
        """
        if not path:
            raise ParamNoneError
        url = urljoin(self.url, self.delete_slash_if_needed(path) + "?recursive=true")
        resp = requests.delete(url)
        if not resp.ok:
            return False
        return True

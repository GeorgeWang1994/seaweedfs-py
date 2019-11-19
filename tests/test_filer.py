#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author:    george wang
@datetime:  2019-11-17
@file:      test_filer.py
@contact:   georgewang1994@163.com
@desc:      测试Filer
"""

from seaweedfs.client import *

filer = Filer(host="0.0.0.0")


class TestFiler(object):
    file_name = "test.js"
    file_package = "test"

    def test_ping(self):
        result = filer.ping()
        assert result

    def test_upload(self):
        with open(self.file_name, "wb") as fp:
            fp.write(b"True")
        with open(self.file_name, "rb") as fp:
            result = filer.upload(fp, self.file_name, self.file_package)
            assert result

        os.remove(self.file_name)
        result = filer.exist(self.file_name, self.file_package)
        assert result

    def test_download(self):
        with open(self.file_name, "wb") as fp:
            fp.write(b"True")
        with open(self.file_name, "rb") as fp:
            result = filer.upload(fp, self.file_name, self.file_package)
            assert result

        os.remove(self.file_name)
        ok, result = filer.download(self.file_name, self.file_package)
        assert result
        assert "content" in result
        assert result["content"] == "True"

    def test_delete(self):
        with open(self.file_name, "wb") as fp:
            fp.write(b"True")
        with open(self.file_name, "rb") as fp:
            result = filer.upload(fp, self.file_name, self.file_package)
            assert result

        result = filer.list(self.file_package)
        assert result
        assert result["Path"] == "/%s" % self.file_package
        assert len(result["Entries"]) == 1
        assert result["LastFileName"] == self.file_name

        os.remove(self.file_name)
        result = filer.delete(self.file_name, self.file_package)
        assert result

        result = filer.list(self.file_package)
        assert result
        assert result["Path"] == "/%s" % self.file_package
        assert result["Entries"] is None

    def test_mkdir(self):
        result = filer.mkdir(self.file_package + "1")
        assert result

    def test_list(self):
        result = filer.list(self.file_package)
        assert result
        assert result["Path"] == "/%s" % self.file_package

    def test_delete_folder(self):
        with open(self.file_name, "wb") as fp:
            fp.write(b"True")
        with open(self.file_name, "rb") as fp:
            result = filer.upload(fp, self.file_name, self.file_package)
            assert result

        os.remove(self.file_name)

        result = filer.exist(self.file_name, self.file_package)
        assert result
        result = filer.delete_folder(self.file_package)
        assert result
        result = filer.exist(self.file_name, self.file_package)
        assert not result

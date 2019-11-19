#!/usr/bin/env python
# ** -- coding: utf-8 -- **

"""
@author:    george wang
@datetime:  2019-11-18
@file:      main.py
@contact:   georgewang1994@163.com
@desc:      example
"""

from seaweedfs.client import *

file_name = "a9090050-f5df-413f-9b3a-d72797d524b3.pcap"
file_package = "downloads"

assert os.path.isfile(file_name)

# create Filer object
filer = Filer(host="0.0.0.0")

# ping
result = filer.ping()
assert result

# upload
with open(file_name, "rb") as fp:
    result = filer.upload(fp, file_name, file_package)
    assert result

result = filer.upload(file_name, file_name, file_package)
assert result

# list
result = filer.list(file_package)
assert result
assert result["Path"] == "/%s" % file_package

# download
ok, result = filer.download(file_name, file_package)
assert result
assert "content" in result
assert result["content"]

# delete
result = filer.delete(file_name, file_package)
assert result

# delete folder
result = filer.delete_folder(file_package)
assert result

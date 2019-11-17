# seaweedfs-py

client of seaweedfs

## method

* ping
* upload
* download
* mkdir
* list
* exist
* delete

## usage

```python

from seaweedfs.client import *

file_name = "test.js"
file_package = "test"

# create Filer object
filer = Filer(host="192.168.16.226")

# ping
result = filer.ping()
assert result

# upload
with open(file_name, "w") as fp:
    fp.write("True")
with open(file_name, "r") as fp:
    result = filer.upload(fp, file_name, file_package)
    assert result

# list
result = filer.list(file_package)
assert result
assert result["Path"] == "/%s" % file_package

# download
ok, result = filer.download(file_name, file_package)
assert result
assert "content" in result
assert result["content"] == "True"

# delete
result = filer.delete(file_name, file_package)
assert result

```

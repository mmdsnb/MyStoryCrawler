#!encoding:utf-8

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

register_openers()
params = {"newfile": open(r"Readme.txt", "rb"),"name":"test"}
datagen, headers = multipart_encode(params)
request = urllib2.Request("http://192.168.1.112:12121/files", datagen, headers)
print urllib2.urlopen(request).read()
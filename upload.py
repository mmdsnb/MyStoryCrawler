#!encoding:utf-8

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import zipfile



def upload_file(fileName):
	register_openers()
	params = {"newfile": open(fileName, "rb")}
	datagen, headers = multipart_encode(params)
	request = urllib2.Request("http://192.168.1.112:12121/files", datagen, headers)
	print urllib2.urlopen(request).read()



def write_epub():
	epub = zipfile.ZipFile("testepub", 'w')
	epub.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
	epub.writestr('META-INF/container.xml',' ', compress_type=zipfile.ZIP_STORED)
	epub.writestr('OEBPS/content.opf', compress_type=zipfile.ZIP_STORED)
	epub.close()

write_epub()

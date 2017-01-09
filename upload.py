#!encoding:utf-8

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import zipfile
import epub



def upload_file(fileName):
	register_openers()
	params = {"newfile": open(fileName, "rb")}
	datagen, headers = multipart_encode(params)
	request = urllib2.Request("http://192.168.1.112:12121/files", datagen, headers)
	print urllib2.urlopen(request).read()



def write_epub():
	book = epub.open_epub('book.epub', u'w')
	filename = r'dashengzhuan\add.xhtml'
	manifest_item = epub.opf.ManifestItem(identifier='IdFile',href=r'dashengzhuan\add.xhtml',media_type='application/xhtml+xml')
	book.add_item(filename, manifest_item)
	book.close()

write_epub()

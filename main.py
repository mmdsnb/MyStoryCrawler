#!encoding:utf-8

import upload
import base
import urllib
import re
from prettytable import PrettyTable
import logging
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import storage
import chardet
import sys
import inspect
import os
import tqdm
import numpy
import multiprocessing
from   multiprocessing import Pool


logging.basicConfig(level=logging.WARN)
reload(sys)
sys.setdefaultencoding('utf8')
mtime = base.Mytime()


def getbook(bookname):
	searchUrl = "http://zhannei.baidu.com/cse/search?q=%s&s=5342360055055406737&entry=1"
	html = base.getHtml(searchUrl % (bookname,))
	reStr = '''<a cpos="title" href="(.*?)" title="大圣传" class="result-game-item-title-link" target="_blank">.*?<span class="result-game-item-info-tag-title preBold">作者：</span><span>(.*?)</span>'''
	parttern = re.compile(reStr)
	items = parttern.findall(html)
	return items[0][0];


def getdir(bookurl):
	html = base.getHtml(bookurl)
	logging.info(html)
	reStr = '''<dd><a href=("|')(.*?.html)("|')>(.*?)</a></dd>'''
	parttern = re.compile(reStr)
	items = parttern.findall(html)
	return items


def downloadpage(pageUrl, file_name):
	logging.debug('start download pageUrl: %s' % (pageUrl,))
	# browser = webdriver.PhantomJS()
	# browser.get(pageUrl)
	# html = browser.page_source
	html = base.getHtml(pageUrl)
	if(html is None):
		return
	soup = BeautifulSoup(html, "html.parser")
	items = soup.select('#TXT')
	div = items[0]
	content_tpl = '''
	<html>
		<head>
		  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		</head>
		<body>
			%(content)s
		</body>
	</html>
	'''
	contentStr = str(div.prettify().encode("utf-8"))
	output = open(file_name, 'w+')
	output.writelines(content_tpl % {"content": contentStr})
	output.close()


def startIndex(bookname):
	bookurl = getbook(bookname)
	logging.debug('bookurl %s' % bookurl)
	dirlist = getdir(bookurl)
	logging.info('get indexes end...')
	bookIndexes = list()
	for i in dirlist:
		bookIndex = storage.BookIndex(
		    unicode(bookname), i[3].decode('gbk'), bookurl + i[1])
		bookIndexes.append(bookIndex)

	storage.addBookIndexes(bookIndexes)
	logging.info('storage indexes end...')


def subDownload(bookindex):
	downloadpage(bookindex.url, r"htmls/%d.html" % (bookindex.id,))
	# storage.updateStatus(bookindex)


def startDownload(bookname):
	bookIndexes = storage.getBookIndexesByName(unicode(bookname))
	subc = len(bookIndexes) % 4
	if(subc != 0):
		for i in range(4 - subc):
			bookIndexes.append(None)
	matrix = numpy.array(bookIndexes)
	matrix.shape = -1, 4
	pbar = tqdm.tqdm(range(len(matrix)))
	manager = multiprocessing.Manager()
	for i in pbar:
		pool = Pool()
		param=matrix[i]
		print(param)
		pool.map(subDownload,param)
		pool.close()
		pool.join()
		break
		


def packageEpub(bookname,authorname):
	epubUtil=upload.EpubUtil()
	epubpath=os.path.dirname(inspect.stack()[0][1])+os.path.sep+"books"+os.path.sep+bookname+'.epub'
	epubUtil.createEpub(epubpath)
	epubUtil.setMetadata(bookname,authorname,'this epub created by mmdsnb.')
	htmls =  os.listdir("htmls")
	ids=list()
	for i in htmls:
		ids.append(int(i.split('.')[0]))
	ids.sort()
	for i in ids:
		dirName=storage.getBookIndexById(i).dirName
		epubUtil.addItem(dirName,'htmls'+os.path.sep+"%d.html" % (i,))
	epubUtil.close()



if __name__ == "__main__":
	bookname='大圣传'
	pinyinbookname='xiaoshuopinyingming'
	epubpath="books"+os.path.sep+pinyinbookname+".epub"
	uploadurl="http://xxx.xxx.xxx.xxx:12121/files"
	# startIndex(bookname)
	startDownload(bookname)



# startDownload(bookname)
# packageEpub(pinyinbookname,'说梦者')
# upload.uploadFile(epubpath,uploadurl)






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
import inspect, os

logging.basicConfig(level=logging.DEBUG)
reload(sys)
sys.setdefaultencoding('utf8')


def getbook(bookname):
	searchUrl="http://zhannei.baidu.com/cse/search?q=%s&s=5342360055055406737&entry=1"
	html = base.getHtml(searchUrl  % (bookname,))
	reStr='''<a cpos="title" href="(.*?)" title="大圣传" class="result-game-item-title-link" target="_blank">.*?<span class="result-game-item-info-tag-title preBold">作者：</span><span>(.*?)</span>'''
	parttern= re.compile(reStr)
	items= parttern.findall(html)
	return items[0][0];


def getdir(bookurl):
	html = base.getHtml(bookurl)
	logging.info(html)
	reStr='''<dd><a href=("|')(.*?.html)("|')>(.*?)</a></dd>'''
	parttern= re.compile(reStr)
	items= parttern.findall(html)
	return items


def downloadpage(pageUrl,file_name):
	logging.debug('start download pageUrl: %s' %(pageUrl,))
	browser = webdriver.PhantomJS()
	browser.get(pageUrl)
	html = browser.page_source
	soup=BeautifulSoup(html, "html.parser")
	items= soup.select('#TXT')
	div = items[0]
	content_tpl='''
	<html>
		<head>
		  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		</head>
		<body>
			%(content)s
		</body>
	</html>
	'''
	contentStr=str(div.prettify().encode("utf-8"))
	output = open(file_name, 'w+')
	output.writelines(content_tpl % {"content":contentStr})
	output.close()



def startIndex(bookname):
	bookurl= getbook(bookname)
	logging.debug('bookurl %s' %bookurl)
	dirlist= getdir(bookurl)
	logging.info('get indexes end...')
	bookIndexes=list()
	for i in dirlist:
		bookIndex=storage.BookIndex(unicode(bookname),i[3].decode('gbk'),bookurl+i[1])
		bookIndexes.append(bookIndex)
	
	storage.addBookIndexes(bookIndexes)
	logging.info('storage indexes end...')



def startDownload(bookname):
	bookIndexes = storage.getBookIndexesByName(unicode(bookname))
	index=0
	for i in bookIndexes:
		print(index)
		downloadpage(i.url,r"htmls/%d.html" %(i.id,))
		if(index==10):
			break
		index+=1



def packageEpub(bookname,authorname):
	epubUtil=upload.EpubUtil()
	epubpath=os.path.dirname(inspect.stack()[0][1])+os.path.sep+"books"+os.path.sep+bookname+'.epub'
	epubUtil.createEpub(epubpath)
	epubUtil.setMetadata(bookname,authorname,'this epub created by mmdsnb.')
	htmls =  os.listdir("htmls")
	for i in htmls:
		dirName=storage.getBookIndexById(i.split('.')[0]).dirName
		epubUtil.addItem(dirName,'htmls'+os.path.sep+i)
	epubUtil.close()


bookname='大圣传'
pinyinbookname='dashengzhuan'
epubpath="books"+os.path.sep+pinyinbookname+".epub"
uploadurl="http://192.168.1.111:12121/files"
# startIndex(bookname)
# startDownload(bookname)
# packageEpub(pinyinbookname,'说梦者')
# upload.uploadFile(epubpath,uploadurl)






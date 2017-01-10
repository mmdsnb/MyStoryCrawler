#!encoding:utf-8

import page
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
import sqlite3

logging.basicConfig(level=logging.DEBUG)

def getbook(bookname):
	searchUrl="http://book.easou.com/w/search.html?q=%s&sty=1&f=0"
	html = base.getHtml(searchUrl  % (bookname,))
	reStr=""
	reStr+="<div class=\"name\"><a class=\"common\" href=\"(/w/novel/.*?.html)\">(.*?)</a>"
	reStr+='''<span class=".*?">.*?</span></div><div class="attr"><span class="author">作者：<a class="common" href="/w/searchAuthor/.*?.html">(.*?)</a>'''
	parttern= re.compile(reStr)
	items= parttern.findall(html)
	table=PrettyTable(["url", "name","author"])  

	bookurl=items[0][0]
	for i in items:
		table.add_row(i)

	# logging.debug(table)
	return bookurl

def getdir(bookurl):
	listUrl="http://book.easou.com%s" % (bookurl,)
	html = base.getHtml(listUrl)
	reStr=""
	reStr+='''<a href="(/w/chapter/.*?)">查看目录</a>'''
	parttern= re.compile(reStr)
	items= parttern.findall(html)
	listAllUrl="http://book.easou.com"+items[0]
	logging.debug('get dir listAllUrl:%s' %(listAllUrl,))
	dirlist=list()
	getalldir(listAllUrl,dirlist)
	return dirlist
	

def getalldir(dirurl,dirlist):
	logging.debug("start gethtml %s" %(dirurl,))
	html = base.getHtml(dirurl)
	reStr='''<a class="common" href="(/w/read/.*?.html)">(.*?)</a>'''
	parttern= re.compile(reStr)
	items= parttern.findall(html)
	for i in items:
		dirlist.append(i)

	reStr='''(?<!</span>)<a class="common" href="(/w/chapter/.*?.html)" target="_self"><span class="next">下一页</span></a>'''
	parttern= re.compile(reStr)
	items= parttern.findall(html)
	logging.debug("getalldir items %s" %(items))
	if(len(items)==0):
		return dirlist
	else:
		getalldir("http://book.easou.com"+items[0],dirlist)


def downloadpage(pageUrl,file_name):
	browser = webdriver.PhantomJS()
	browser.get(pageUrl)
	html = browser.page_source
	soup=BeautifulSoup(html, "html.parser")
	items= soup.select('div[class="content"]')
	div = items[0]
	del div['class']
	del div['style']
	for i in  div.find_all(['div','script']):
		i.extract()

	contentStr=str(div.prettify().encode("utf-8"))
	contentStr=contentStr.replace("<br>",'')
	contentStr=contentStr.replace("</br>",'')
	contentStr=contentStr.replace("<div>",'')
	contentStr=contentStr.replace("</div>",'')
	contentStr=contentStr.replace(" ",'')
	output = open(file_name, 'w+')
	output.writelines(contentStr)
	contentlist=list()
	for subline in contentStr.splitlines():
		if(subline != '\n' and subline != ''):
			contentlist.append(subline+"\n")
		
	contentStr="".join(contentlist)
	print(contentStr)
	output.close()



def main():
	bookurl= getbook('大圣传')
	logging.debug('bookurl %s' %bookurl)
	dirlist= getdir(bookurl)
	print(len(dirlist))
	print(dirlist[0][0])



# downloadpage('http://book.easou.com/w/read/8140825/10811075/1667.html',r'd:\a.txt')


conn = sqlite3.connect("test.db")
# conn.execute('''CREATE TABLE t_user
#        (ID INT PRIMARY KEY     NOT NULL,
#        NAME           TEXT    NOT NULL,
#        AGE            INT     NOT NULL,
#        ADDRESS        CHAR(50));''')
conn.execute('''insert into t_user values(1,'a',12,'abc')''');
cursor = conn.execute("SELECT *  from t_user")
table=PrettyTable(["id", "name","age","address"])  
for row in cursor:
	table.add_row(row)
print(table)
conn.commit()






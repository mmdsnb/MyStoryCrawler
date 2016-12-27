#!encoding:utf-8


import urllib
import re
from prettytable import PrettyTable 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


searchUrl="http://book.easou.com/w/search.html?q=%s&sty=1&f=0"
def getHtml(url):
	response = urllib.urlopen(url)
	html = response.read()
	return html



html = getHtml(searchUrl  % ("大圣",))
reStr=""
reStr+="<div class=\"name\"><a class=\"common\" href=\"/w/novel/(.*?.html)\">(.*?)</a>"
reStr+='''<span class=".*?">.*?</span></div><div class="attr"><span class="author">作者：<a class="common" href="/w/searchAuthor/.*?.html">(.*?)</a>'''
parttern= re.compile(reStr)
items= parttern.findall(html)
table=PrettyTable(["url", "name","author"])  

for i in items:
	table.add_row(i)

print(table)





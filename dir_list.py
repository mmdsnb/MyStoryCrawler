#!encoding:utf-8
import urllib
import re
from prettytable import PrettyTable 
import base

listUrl="http://book.easou.com/w/novel/%s"

html = base.getHtml(listUrl % ('8140825/0.html',))
reStr=""
reStr+='''<a href="(/w/chapter/.*?)">查看目录</a>'''
parttern= re.compile(reStr)
items= parttern.findall(html)
listAllUrl="http://book.easou.com"+items[0]

html = base.getHtml(listAllUrl)
reStr='''<a class="common" href="(/w/read/.*?.html)">(.*?)</a>'''
parttern= re.compile(reStr)
items= parttern.findall(html)
table=PrettyTable(["url", "name"])  
for i in items:
	# print(i)
	table.add_row(i)
	break

print(table)
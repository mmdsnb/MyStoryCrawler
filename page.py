#!encoding:utf-8


import base
import re

pageUrl="http://book.easou.com/w/read/8140825/10811075/1666.html"

html = base.getHtml(pageUrl)
# print(html)
reStr='''>"\);</script>(.*?)<div class="footerbar">'''
parttern= re.compile(reStr)
items = parttern.findall(html)
print(items[0])


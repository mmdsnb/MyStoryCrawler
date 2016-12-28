#!encoding:utf-8


import base
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time

pageUrl="http://book.easou.com/w/read/8140825/10811075/1666.html"
browser = webdriver.PhantomJS()
browser.get(pageUrl)
# print(browser.page_source)
html = browser.page_source
# print(html)
# reStr='''>"\);</script>(.*?)<div class="footerbar">'''
# parttern= re.compile(reStr)
# items = parttern.findall(html)
# print(items[0])

soup=BeautifulSoup(html, "html.parser")
items= soup.select('div[class="content"]')
div = items[0]
del div['class']
del div['style']
for i in  div.find_all(['div','script']):
	i.extract()
print(div)


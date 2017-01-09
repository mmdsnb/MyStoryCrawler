#!encoding:utf-8


import base
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import upload
import chardet


def download_page(pageUrl,file_name):
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
	# print(contentStr)
	output.close()




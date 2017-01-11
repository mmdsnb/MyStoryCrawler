#!encoding:utf-8
import urllib


def getHtml(url):
	response = urllib.urlopen(url)
	html = response.read()
	return html

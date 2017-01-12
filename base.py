#!encoding:utf-8
import urllib
import urllib2



def mutilLineToOne(strs):
	lines=list()
	for l in strs.splitlines():
		lines.append(l.strip())

	return ''.join(lines)


def getHtml(url):  
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'     
	headers = { 'User-Agent' : user_agent }  
	req = urllib2.Request(url=url, headers=headers)   
	response = urllib2.urlopen(req)   
	the_page = response.read() 
	return mutilLineToOne(the_page)





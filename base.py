#!encoding:utf-8
import urllib
import urllib2
import logging
import time

logging.basicConfig(level=logging.ERROR)
def mutilLineToOne(strs):
	lines=list()
	for l in strs.splitlines():
		lines.append(l.strip())

	return ''.join(lines)


def getHtml(url):  
	try:
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'     
		headers = { 'User-Agent' : user_agent }  
		req = urllib2.Request(url=url, headers=headers)   
		response = urllib2.urlopen(req,timeout=5)   
		the_page = response.read() 
		return the_page
	except Exception as e:
		logging.error('time out url :%s' %(url,))

	return None
	
class Mytime:

	current_time=time.time()

	def init(self):
		self.current_time=time.time()

	def getsubtime(self,*prefix):
		subtime=time.time()-self.current_time
		self.current_time=time.time()
		print("%s : %f" %(prefix,subtime))



def tyield():
	sumval=1
	for i in range(5):
		yield sumval
		sumval=sumval+1
	

for i in tyield():
	print(i)
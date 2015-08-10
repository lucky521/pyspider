__author__ = "Lucky"
## -*- coding:utf-8 -*-
# Get article Names from my CSDN blog

import urllib
import urllib2
import re,time
import threading

class Collector:
	def __init__(self):
		self.article_number = 0
		self.article_name = []

	def add(self, name):
		self.article_number += 1
		self.article_name.append(name)
		return 


collector = Collector()


class Spider:
	def __init__(self):
		self.siteURL = 'http://blog.csdn.net/luckyjoy521/article/list/'
		self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}

	def getPage(self, pageIndex):
		url = self.siteURL + "" + str(pageIndex)
		request = urllib2.Request(url, headers=self.hdr)
		for i in range(1,4):
			try:
				response = urllib2.urlopen(request, timeout=8) #timeout
				page = response.read()
				print url
				return page
			except Exception, e:
				time.sleep(8)
				print str(e) +  " Retry to " + url

		print "Connection Failed to " + url
		return ""


	def getContent(self, pageIndex):
		page = self.getPage(pageIndex)
		
		#grep certain content
		pattern = re.compile("(?<=link_title).*\n.*(?=\n)")
		items = re.findall(pattern, page)
		for item in items:
			it = item.split("\n")
			an = it[1].strip()
			print an
			collector.add(an)
		
		#record page
		f1 = file("page_" + str(pageIndex) + ".html", "w")
		f1.write(page)
		f1.close
		return



def worker(index):
	spd = Spider()
	spd.getContent(index)
	return 


if __name__ == "__main__":
	threads = []
	for i in range(1,18):
		t = threading.Thread(target=worker, args=(i,))
		threads.append(t)
		t.setDaemon(True)   # So thread can be terminated by Ctrl+C
		t.start() 

	for t in threads:
		t.join(600)

	print collector.article_number



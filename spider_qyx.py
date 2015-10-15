__author__ = "Lucky"
## -*- coding:utf-8 -*-

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
		self.siteURL = 'http://www.qyx888.com/thread-195166-1-1.html'
		self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
				'Accept-Encoding': 'none', 
				'Accept-Language': 'en-US,en;q=0.8', 
				'Connection': 'keep-alive'}

	def getPage(self, pageIndex):
		url = self.siteURL + "" #str(pageIndex)
		request = urllib2.Request(url, headers=self.hdr)
		# If fail or timeout, Retry for 3 times
		for i in range(1,4):
			try:
				response = urllib2.urlopen(request, timeout=8)
				page = response.read()
				print  "Succeed to " + url
				return page
			except Exception, e:
				time.sleep(8)
				print str(e) +  " Retry to " + url
		print "Connection Failed to " + url
		return ""

	def handle_DIY(self, content):
		pattern1 = re.compile("^.*[0-9]*(?=\")")
		match1 = pattern1.search(content)
		url = "http://www.zhihu.com"+ match1.group()

		pattern2 = re.compile("(?<=>).*$")
		match2 = pattern2.search(content)
		title = match2.group()
		result = "[%s](%s)\n\n" %(title,url)
		return result
	
	def outtofile(self, filename, content):
		#record page
		f1 = file(filename, "a")
		f1.write(content)
		f1.close
		return

	def getContent(self, pageIndex):
		page = self.getPage(pageIndex)
		#print page
		#grep certain content
		lookbehind = "<div class=\"sign\""
#		lookbehind = "<div class=\"sign\" style=\"max-height:150px;maxHeightIE:150px;\"><strong><font size=\"3\">"

#		lookbehind = "zm-item-title\"><a target=\"_blank\" href=\"" 
		lookahead = "</font></strong></div>"
		regex = ".*"
		pattern = re.compile("(?<=" + lookbehind +")" + regex + "(?=" + lookahead +")")
		items = re.findall(pattern, page)
		for item in items:
			print item
			collector.add(item)
			#diy = self.handle_DIY(item)
			self.outtofile("collection01.md", diy)
		return



def worker(index):
	spd = Spider()
	spd.getContent(index)
	return 


if __name__ == "__main__":
	threads = []
	for i in range(1,2):
		t = threading.Thread(target=worker, args=(i,))
		threads.append(t)
		t.setDaemon(True)   # So thread can be terminated by Ctrl+C
		t.start() 

	for t in threads:
		t.join(600)

	print collector.article_number


__author__ = "Lucky"
## -*- coding:utf-8 -*-

import urllib
import urllib2
import re

class Spider:
	def __init__(self):
		self.siteURL = 'http://blog.csdn.net/luckyjoy521/article/list/'
		self.article_number = 0
		self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}

	def getPage(self, pageIndex):
		url = self.siteURL + "" + str(pageIndex)
		print url

		request = urllib2.Request(url, headers=self.hdr)
		response = urllib2.urlopen(request)
		return response.read()#.decode('gbk')

	def getContent(self, pageIndex):
		page = self.getPage(pageIndex)
		
		#grep certain content
		pattern = re.compile("(?<=link_title).*\n.*(?=\n)")
		items = re.findall(pattern, page)
		for item in items:
			it = item.split("\n")
			print it[1].strip()
			self.article_number += 1
		
		#record page
		f1 = file("page_" + str(pageIndex) + ".html", "w")
		f1.write(page)
		f1.close
		return 

if __name__ == "__main__":
	spd = Spider()
	for i in range(1, 2):
		spd.getContent(i)
	print spd.article_number

__author__ = "Lucky"
## -*- coding:utf-8 -*-
import urllib
import urllib2
import re,time
import threading
##############################################
#template
class PageLib:
		def __init__(self):
			self.page_set = set()
			return
		def inLib(self, url):
			if url in self.page_set:
				return True
			else:
				return False	

		def storePage(self, url):
			self.page_set.add(url)
			return

# global 
pagelib = PageLib()


class Collector:
	def __init__(self):
		self.article_number = 0
		self.article_name = []

	def add(self, name):
		self.article_number += 1
		self.article_name.append(name)
		return 

# global
collector = Collector()



class Spider:
	def __init__(self):
		self.baseURL = 'http://www.qyx888.com/'
		self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Charset': 'ISO-8859-1,gbk;q=0.7,*;q=0.3', 
				'Accept-Encoding': 'none', 
				'Accept-Language': 'en-US,en;q=0.8', 
				'Connection': 'keep-alive'}
		return


	def match_forum_page(self, page):
		match_set = set()
		# http://www.qyx888.com/forum-19-1.html
		regex = self.baseURL + "forum-[0-9][0-9]*-1.html"
		pattern = re.compile(regex)
		items = re.findall(pattern, page)
		for item in items:
			print "match" + str(item)
			match_set.add(item)
		return match_set

	def match_thread_page(self, page):
		# http://www.qyx888.com/thread-405018-1-1.html
		match_set = set()
		regex = self.baseURL + "thread-[0-9][0-9]*-1.html"
		pattern = re.compile(regex)
		items = re.findall(pattern, page)
		for item in items:
			#print "match" + str(item)
			match_set.add(item)
		return match_set


	def getPage(self, url):
		request = urllib2.Request(url, headers=self.hdr)
		# If fail or timeout, Retry for 3 times
		for i in range(1,4):
			try:
				response = urllib2.urlopen(request, timeout=8)
				page = response.read()
				print  "Succeed to get page: " + url
				return page.decode('gbk')
			except Exception, e:
				time.sleep(8)
				print str(e) +  " Retry to " + url
		print "Connection Failed to " + url
		return ""

	def handle_DIY(self, content):
		result = content
		'''
		pattern1 = re.compile("^.*[0-9]*(?=\")")
		match1 = pattern1.search(content)
		url = "http://www.zhihu.com"+ match1.group()

		pattern2 = re.compile("(?<=>).*$")
		match2 = pattern2.search(content)
		title = match2.group()
		result = "[%s](%s)\n\n" %(title,url)
		'''
		return result
	
	def outtofile(self, filename, content):
		f1 = file(filename, "a")
		f1.write(content + '\n')
		f1.close
		return

	def getContent_from_page(self, page):
		#grep certain content
		lookbehind = "<div class=\"sign\" style=\"max-height:150px;maxHeightIE:150px;\">"
#		lookbehind = "<div class=\"sign\" style=\"max-height:150px;maxHeightIE:150px;\"><strong><font size=\"3\">"
#		lookbehind = "zm-item-title\"><a target=\"_blank\" href=\"" 
		lookahead = "</div>\r\n</td>\r\n</tr>\r\n<tr id=\"_postposition"
		regex = "[\s\S]*?"
		pattern = re.compile("(?<=" + lookbehind +")" + regex + "(?=" + lookahead +")")
		items = re.findall(pattern, page)
		for item in items:
			#print item
			collector.add(item)
			diy = self.handle_DIY(item)
			self.outtofile("collected_data.md", diy.encode('utf-8'))
		return


	def getContent_from_url(self, pageIndex):
		page = self.getPage(pageIndex)
		#print page
		#self.outtofile("tmp.md", page.encode('utf-8'))

		#grep certain content
		lookbehind = "<div class=\"sign\" style=\"max-height:150px;maxHeightIE:150px;\">"
#		lookbehind = "<div class=\"sign\" style=\"max-height:150px;maxHeightIE:150px;\"><strong><font size=\"3\">"
#		lookbehind = "zm-item-title\"><a target=\"_blank\" href=\"" 
		lookahead = "</div>\r\n</td>\r\n</tr>\r\n<tr id=\"_postposition"
		regex = "[\s\S]*?"
		pattern = re.compile("(?<=" + lookbehind +")" + regex + "(?=" + lookahead +")")
		items = re.findall(pattern, page)
		for item in items:
			#print item
			collector.add(item)
			diy = self.handle_DIY(item)
			self.outtofile("collected_data.md", diy.encode('utf-8'))
		return


	def get_all_url_in_current_page(self, page):
		new_url_set = set()
		#match url and store new urls
		for url in self.match_thread_page(page):
			if not pagelib.inLib(url):
				new_url_set.add(url)

		for url in self.match_forum_page(page):
			if not pagelib.inLib(url):
				new_url_set.add(url)

		print "Find new urls: " + str(new_url_set)
		return new_url_set


	def start_work(self):
		front_page = self.getPage(self.baseURL + "forum.php") # front page
		new_url1 = self.get_all_url_in_current_page(front_page)
		new_url2 = set()

		if len(new_url1) > 0: 
			time.sleep(1)
			for url in new_url1:
				print "surf to " + str(url)
				# get page just once
				page = self.getPage(url)
				# get new url from page
				new_url2 = new_url2.union(self.get_all_url_in_current_page(page))
				# get target data from page
				self.getContent_from_page(page)
				# mark this page as old
				pagelib.storePage(url)
			new_url1 = new_url2

		return


#######################################################
def worker(index):
	spd = Spider()
	#spd.getContent(index)
	spd.start_work()
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


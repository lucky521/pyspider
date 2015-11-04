__author__ = "Lucky"
## -*- coding:utf-8 -*-
import urllib
import urllib2
import re,time
import threading
from copy import deepcopy
##############################################
# template class for global & common resource

# record urls
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

# collect target data
class Collector:
	def __init__(self):
		self.data = set()
	def add(self, name):
		self.data.add(name)
		return
	def isExist(self, name):
		if name in self.data:
			return True
		else:
			return False

# global
collector = Collector()


class Logger():
	def __init__(self):
		self.timeout_times = 0

	def connection_timeout(self):
		self.timeout_times += 1

# global
logger = Logger()

##############################################

class Spider:
	def __init__(self):
		self.baseURL = 'http://www.xxx.com/'
		self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Charset': 'ISO-8859-1,gbk;q=0.7,*;q=0.3', 
				'Accept-Encoding': 'none', 
				'Accept-Language': 'en-US,en;q=0.8', 
				'Connection': 'keep-alive'}
		return

	#TODO: this can be utility
	def match_forum_page(self, page):
		# http://www.xxx.com/forum-19-1.html
		match_set = set()
		regex = "forum-[0-9]+-1.html"
		pattern = re.compile(regex)
		items = re.findall(pattern, page)
		for item in items:
			#print "match " + str(item)
			match_set.add(item)
		return match_set

	#TODO: this can be utility
	def match_thread_page(self, page):
		# http://www.xxx.com/thread-405018-1-1.html
		match_set = set()
		regex = "thread-[0-9]+-[0-9]+-1.html"
		pattern = re.compile(regex)
		items = re.findall(pattern, page)
		for item in items:
			#print "match" + str(item)
			match_set.add(item)
		return match_set


	def getPage(self, url):
		# return page data from url, do nothing else
		url = self.baseURL + url
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
		logger.connection_timeout()
		return ""


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
		print "get data: " + str(len(items))
		for item in items:
			#print item
			if not collector.isExist(item):
				collector.add(item)
				self.outtofile("tmp_collected_data.md", item.encode('utf-8')+ "\r\n\r\n")
		return


	def get_all_url_in_current_page(self, page):
		new_url_set = set()
		# match url and just store new urls
		for url in self.match_thread_page(page):
			if not pagelib.inLib(url):
				new_url_set.add(url)

		for url in self.match_forum_page(page):
			if not pagelib.inLib(url):
				new_url_set.add(url)

		print "Find new urls: " + str(len(new_url_set))
		return new_url_set


	def start_work(self):
		front_url = "thread-414645-17-1.html" # front page
		front_page = self.getPage(front_url)   
		self.getContent_from_page(front_page)
		pagelib.storePage(front_url)
		new_url1 = deepcopy(self.get_all_url_in_current_page(front_page))
		new_url2 = set()

		while len(new_url1) > 0:
			time.sleep(2)
			tmp_list = list(new_url1)
			tmp_list.sort(reverse=True)
			for url in tmp_list:
				time.sleep(1)
				if pagelib.inLib(url):
					continue
				print "surf to " + str(url)
				# get page just once
				page = self.getPage(url)
				# mark this page as old
				pagelib.storePage(url)
				# get new url from page
				new_url2 = deepcopy(new_url2 | self.get_all_url_in_current_page(page))
				# get target data from page
				self.getContent_from_page(page)

			new_url1.clear()
			new_url1 = deepcopy(new_url2) # deep copy
			new_url2.clear()
			print "***************************urls left to access: " + str(len(new_url1))

		# list all the url
		print "\n\npage num: " + str(len(pagelib.page_set))
		for url in pagelib.page_set:
			self.outtofile("tmp_pagelib.md", url)

		return


#######################################################
# utilities

def backupfile(sfile, dfile):
	file1 = file(sfile)
	file2 = file(dfile, 'w')
	for it in file1:
		file2.write(it)
	file1.close()
	file2.close()
	open(sfile,'w').close()
	return


#######################################################
# -- main and worker thread
# target webside may be not fast to access
# and I do not let them notice me
# so I do not use multi-thread now
def worker(index):
	spd = Spider()
	spd.start_work()
	return


if __name__ == "__main__":
	threads = []
	for i in range(1,2): # thread num
		t = threading.Thread(target=worker, args=(i,))
		threads.append(t)
		t.setDaemon(True)   # So thread can be terminated by Ctrl+C
		t.start() 

	for t in threads:
		t.join()

	backupfile("tmp_collected_data.md", "result_data.md")
	backupfile("tmp_pagelib.md", "result_urls.md")

	print "Taks Done. Data number:" + str(len(collector.data))
	print "timeout times: " + str(logger.timeout_times)

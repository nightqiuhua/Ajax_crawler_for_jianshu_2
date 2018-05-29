import re 
import urllib.parse 
import urllib.request 
import datetime 
import time 
from downloader_p3 import Downloader
from mogon_cache import MongoCache
from scrape_callback2_p3 import ScrapeCallback
import lxml.html


def link_crawler(seed_url,page,link_regx=None,delay=5,max_depth=2,max_urls=-1,user_agent=None,proxies=None,num_retries=1,scrape_callback=None,cache=None):
	D = Downloader(delay=delay,user_agent=user_agent,proxies=proxies,num_tries=num_retries,cache=cache)
	try:
		user_id = seed_url.split(r'/')
		user_id = user_id[4]
		if seed_url.find('page='):
			page = page +1
		html = D(seed_url).decode('utf-8')
		if scrape_callback:
			scrape_callback.__call__(html)
	except Exception as e:
		raise e
	else:
		tree = lxml.html.fromstring(html)
		id_infos = tree.xpath('//ul[@class="note-list"]/li/@id')
		if len(id_infos) > 1:
			feed_id = id_infos[-1]
			max_id = feed_id.split('-')[1]
			max_id = int(max_id)-1
			next_url = 'https://www.jianshu.com/users/{}/timeline?max_id={}&page={}'.format(user_id,max_id,page)
			link_crawler(next_url,page,link_regx,delay,max_depth,max_urls,user_agent,proxies,num_retries,scrape_callback,cache)

seed_url = 'http://www.jianshu.com/users/9104ebf5e177/timeline'
page = 1
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
link_crawler(seed_url=seed_url,page = 1,user_agent=user_agent,scrape_callback=ScrapeCallback(),cache = MongoCache())
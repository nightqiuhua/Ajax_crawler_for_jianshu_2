import csv 
import re 
import lxml.html 
import urllib.parse
from pymongo import MongoClient
from datetime import datetime,timedelta
import pymongo

class ScrapeCallback:
	def __init__(self,client=None,expires=timedelta(days=30)):
		self.db = pymongo.MongoClient("localhost",27017).cache
		self.db.timeline.create_index('timestamp',expireAfterSeconds=expires.total_seconds())

	def __call__(self,html):
		try:
			tree = lxml.html.fromstring(html)
			infos = tree.xpath('//ul[@class="note-list"]/li')
			for info in infos:
				dd = info.xpath('./div/div/div/span/@data-datetime')[0]
				file_type = info.xpath('./div/div/div/span/@data-type')[0]
				self.db.timeline.insert_one({'date':dd,'type':file_type})
		except Exception as e:
			raise e
		
		


import scrapy
import json
import os
import logging

logger = logging.getLogger(__name__)
def_format = logging.Formatter(fmt="[%(asctime)s][%(levelname)s]:%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
def_handler = logging.FileHandler("../../data/serverlog.log")
def_handler.setLevel(logging.DEBUG)
def_handler.setFormatter(def_format)
logger.addHandler(def_handler)

items = {}

class animeDownloader(scrapy.Spider):
	name = 'data'
	start_urls = [
		"https://horriblesubs.info/"
	]

	#Function to parse current season list
	def parse_season(self, response):
		global items
		# items = CurrentSeasonItem()
		items['current_season'] = response.xpath('//div[@class="ind-show"]/a/@title').extract()
		#print(type(items))
		with open('../../data/data.json', 'w') as f:
			json.dump(items, f, indent=4)
		yield items

	#Function to parse schedule and time of shows
	def parse(self, response):
		global items
		# items = ScheduleTimeItem()

		#Get Schedule for the day
		schedule = response.xpath('//table[@class="schedule-table"]/tr/td/a/text()').extract()
		release_time = response.xpath('//table[@class="schedule-table"]/tr/td/text()').extract()
		items['timetable'] = dict(zip(schedule, release_time))
		#print('WORKING DIR: ' + os.getcwd())
		yield items

		#Get Current Season
		season = response.xpath('//ul/li/a[@title="Shows airing this season"]/@href').extract_first()
		yield scrapy.Request(season, callback = self.parse_season)
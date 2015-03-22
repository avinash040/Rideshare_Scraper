import scrapy
import re
from .. import items

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class KijijiRideshareSpider(CrawlSpider):
	"""
	*A scrapy crawler to extract rideshare information from kijiji
	*Crawls the kijiji wepages to find rideshare information
	*currently, only supports Ottawa
	"""
	name = "kijiji_rideshare_spider"
	allowed_domains = ['kijiji.ca']
	start_urls = ["http://www.kijiji.ca/b-rideshare-carpool/ottawa/c5l1700185"]
	rules = [
			Rule(
				LinkExtractor(
					allow=['http://www.kijiji.ca/v-rideshare-carpool/ottawa/.+']
				),
			callback='parse_rideshare'),
			Rule(
           		LinkExtractor(
                	allow=["http://www.kijiji.ca/b-rideshare-carpool/ottawa/page-[0-9]/.+"]
            	),
            ),
	]

	def parse_item(self, response): 
		"""
		*An earlier version of the code that uses hxs selector 
		*based on code from Github: mjhea0/Scrapy-Samples
		*Not used currently, but left alone for debugging and initial help purpose
		"""
		selection = scrapy.Selector(response)
		titles = selection.xpath("//td[@class='description']")
		result = []
		for title in titles:
			item = items.KijijiRideshareItem()
			item ["title"] = title.select("a/text()").extract()
			item ["link"] = title.select("a/@href").extract()
			result.append(item)
		return result

	def parse_rideshare(self, response):
		"""
		Parses and stores the required rideshare information 
		"""
		rideshare_item = items.kijijiRideshareData()
		rideshare_item["url"] = response.url
		rideshare_item["title"] = self._extract_title(response)
		rideshare_item["date_listed"] = self._extract_field(response, "Date Listed")
		rideshare_item["address"] = self._extract_field(response, "Address")
		rideshare_item["phone_number"] = self._extract_phone_number(response)
		rideshare_item["full_text"] = self._extract_full_text(response)
		return rideshare_item

	def _extract_title(self, response):
		l = " ".join(response.xpath("//h1/text()").extract())
		return self._clean_string(l)
        
	def _extract_full_text(self, response):
		l = " ".join(response.xpath("//span[@itemprop='description']/text()").extract())
		return self._clean_string(l)

	def _extract_phone_number(self, response):
		return "613"

	def _extract_field(self, response, fieldname):
		l = response.xpath("//th[contains(text(), '{0}')]/following::td[1]//./text()".
                format(fieldname)).extract()
		return l[0].strip() if l else None

	def _clean_string(self, string):
		for i in [",", "\n", "\r", ";", "\\"]:
			string = string.replace(i, "")
		return string.strip()


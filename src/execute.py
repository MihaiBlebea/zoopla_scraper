from requests_html import HTMLSession
import json
import time
from datetime import datetime
from lxml import html
import logging
import math
import argparse
from pathlib import Path
from dataclasses import dataclass

from store import insert_listing
from models import Listing


logging.basicConfig(
	filename="scraper.log", 
	level=logging.ERROR, 
	format="%(asctime)s - %(message)s", datefmt="%d-%b%y %H:%M:%S",
)

BASE_URL = "https://www.zoopla.co.uk"
CACHE_FOLDER = "__html_cache__"
JSON_FOLDER = "__json_output__"

@dataclass
class Result:
	id: str
	price: int
	title: str
	url: str
	bath_count: int
	bedroom_count: int
	reception_count: int
	address: str
	phone: str

def main():
	start_time = time.time()

	parser = argparse.ArgumentParser(
		prog= "scraper", 
		usage="%(prog)s [options]", 
		description="running a scraper to get house prices.",
	)

	parser.add_argument(
		"-u",
		dest="url",
		required=True, 
		help="url to scrape",
	)

	args = parser.parse_args()

	url = args.url.replace(BASE_URL, "")

	now = datetime.today()
	time_format = now.strftime("%b-%d-%Y %H:%M:%S")
	print(f"Start scraping url {url} at {time_format}")

	s = HTMLSession()

	# get total page count
	page_count = get_total_page_count(s, url)

	results = []
	for p in range(page_count):
		page = p + 1
		print(f"Scrape page number {page}")

		result = extract_page_data(s, url, page)
		results += result

	for r in results:
		listing = Listing(
			r.id,
			r.price,
			r.title,
			r.url,
			r.bath_count,
			r.bedroom_count,
			r.reception_count,
			r.address,
			r.phone
		)

		insert_listing(listing)

	print("Complete scraping")
	print("--- %s seconds ---" % (time.time() - start_time))


def get_total_page_count(s, url : str) -> int:
	per_page = 25

	raw_html = fetch_html_cache(s, url, 1)

	tree = html.fromstring(raw_html)

	total_count = parse_total_listing_count(
		tree.xpath(
			'//*[@id="__next"]/div[4]/div[2]/main/div[1]/div[2]/div[1]/p', 
			first=True
		)[0].text
	)

	return math.ceil(total_count / per_page)


def extract_page_data(s, url : str, page : int) -> list:
	raw_html = fetch_html_cache(s, url, page)

	tree = html.fromstring(raw_html)
	container = tree.xpath('//*[@id="__next"]/div[4]/div[2]/main/div[2]/div[2]')[0]

	listings = container.getchildren()

	results = []
	for c in listings:
		url = fetch_urls(c)
		results.append(Result(
			extract_id_from_url(url),
			fetch_prices(c),
			fetch_titles(c),
			url,
			fetch_baths(c),
			fetch_bedrooms(c),
			fetch_receptions(c),
			fetch_addresses(c),
			fetch_phones(c),
		))

	return results


def fetch_prices(container) -> int:
	div = container.xpath('./div/div[2]/div[2]/a[2]/div[1]/div')
	ps = div[0].getchildren()
	price = ps[-1].text

	return parse_price(price)


def fetch_bedrooms(container) -> int:
	count = container.xpath('./div[1]/div[2]/div[2]/a[2]/div[2]/div[1]/p')
	if len(count) > 0:
		return int(count[0].text)
	
	return None


def fetch_baths(container) -> int:
	count = container.xpath('./div[1]/div[2]/div[2]/a[2]/div[2]/div[2]/p')
	if len(count) > 0:
		return int(count[0].text)
	
	return None


def fetch_receptions(container) -> int:
	count = container.xpath('./div[1]/div[2]/div[2]/a[2]/div[2]/div[3]/p')
	if len(count) > 0:
		return int(count[0].text)

	return None


def fetch_titles(container) -> str:
	title = container.xpath('./div/div[2]/div[2]/a[2]/h2')[0]

	return title.text


def fetch_addresses(container) -> str:
	address = container.xpath('./div/div[2]/div[2]/a[2]/p')[0]
	
	return address.text


def fetch_phones(container) -> str:
	phone = container.xpath('./div/div[3]/div[2]/a[1]')[0]
	
	return phone.get("href").split(":")[-1]


def fetch_urls(container) -> str:
	url = container.xpath('./div/div[2]/div[2]/a[2]')[0]

	return url.get("href")


def fetch_images(container) -> list:
	results = []
	pics = container.findall("picture")
	
	# ol = container.xpath('./div[1]/div[2]/div[1]/div[1]/div[1]/a/div/div/div[1]/div/ol')
	# if len(ol) == 0:
	# 	ol = container.xpath('./div[1]/div[2]/div[2]/div[1]/div/div[1]/a/div/div/div[1]/div/ol')
	# print(ol)
	# imgs = ol.findall("img")

	# for img in imgs:
	# 	src = img.get("src")
	# 	results.append(src)

	return results


def extract_id_from_url(url : str) -> str:
	return url.strip("/").split("/")[-1]


def parse_price(price_raw : str) -> int:
	if price_raw == "POA":
		return None

	return int(price_raw.replace("£", "").replace(",", ""))


def parse_total_listing_count(value : str) -> int:
	return int(value.split(" ")[0])


def fetch_html_cache(s, url, page = 1):
	Path(f"./{CACHE_FOLDER}").mkdir(parents=True, exist_ok=True)

	date = datetime.today().strftime("%b_%d_%Y")
	file_name = f"{url.strip('/').replace('/', '_')}_{page}_{date}.html"

	cache_file = Path(f"./{CACHE_FOLDER}/{file_name}")
	if cache_file.is_file():
		f = open(f"./{CACHE_FOLDER}/{file_name}", "r")

		return f.read()

	with open(f"./{CACHE_FOLDER}/{file_name}", "w") as outfile:
		r = s.get(f"{BASE_URL}{url}?pn={page}")

		r.html.render(sleep=0, timeout=200)

		outfile.write(r.html.html)
		outfile.close()

	return r.html.html


if __name__ == "__main__":
	main()
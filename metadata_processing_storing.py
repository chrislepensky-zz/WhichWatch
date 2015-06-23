from pymongo import MongoClient
from bson.objectid import ObjectId
from bs4 import BeautifulSoup
import os
import re

client = MongoClient('mongodb://localhost:27017/')
db = client['watches']


file_lst = os.listdir('./data/')
html_file_names = filter(lambda name: name.endswith('.html'), file_lst)

for i, f in enumerate(html_file_names):

	soup = BeautifulSoup(open('data/watch%d.html' % i).read(), 'html.parser')

	watch_brand_metadata = soup.select('.pdp_col_content h1')
	watch_brand = {}
	brand = 'Brand:'
	watch_brand[brand] = [tag.text.strip() for tag in watch_brand_metadata]

	watch_name_metadata = soup.select('.pdp_col_content h2')
	watch_name = {}
	name = 'Watch Name:'
	watch_name[name] = [tag.text.strip() for tag in watch_name_metadata]

	watch_price_metadata = soup.select('.price')
	watch_price = {}
	price = 'Price:'
	watch_price[price] = [tag.text.strip() for tag in watch_price_metadata]

	watch_overview_metadata = soup.select('.prod_details_box_content p')
	watch_overview = {}
	overview = 'Overview:'
	watch_overview[overview] = [tag.text.strip() for tag in watch_overview_metadata]

	#specs

	switch = 0
	tags = soup.select('.box  ul li')
	d = {}
	for tag in tags:
		try:
			watch_id = i
			field, value = tag.text.split(':', 1) 
			field = field.strip()
			value = re.sub('^[a-zA-Z0-9]*$', ' ', value).strip()
			d[field] = value
			d['_id'] = watch_id
		except:
			print '%d did not work' % i
			switch = 1

	if not switch:
		watch_dict = dict(watch_brand.items() + watch_name.items() + watch_price.items() \
			+ watch_overview.items() + d.items())
		db.watches.insert(watch_dict)

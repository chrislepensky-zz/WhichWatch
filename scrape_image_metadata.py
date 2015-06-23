import requests
from bs4 import BeautifulSoup
import os
 

def pull_thumbnails(thumbnail_link, idx):
	pic = requests.get(thumbnail_link).content
	f = open('/Volumes/MacintoshHD/Users/Chris/Desktop/images/watch%i.png' %idx, 'w')
	f.write(pic)
	f.close()

def pull_metadata(metadata_link, idx):
	html = requests.get(metadata_link).content
	f = open('/Volumes/MacintoshHD/Users/Chris/Desktop/images/watch%s.html' %idx, 'w')
	f.write(html)
	f.close()

root_url = 'h'

url = 'a watch site....'
html = requests.get(url).text
 
soup = BeautifulSoup(html, 'html.parser')

thumbnail_tag = soup.select('.current-product.medium .image-display .pdpLink img')
thumbnail_links = [tag['src'] for tag in thumbnail_tag]


metadata_link_tag = soup.select('.current-product.medium .image-display .pdpLink')
metadata_links = [root_url + tag['href'].lstrip('/') for tag in metadata_link_tag]

print metadata_links[:5]

it = 0
for thumbnail_link, metadata_link in zip(thumbnail_links, metadata_links):
	pull_thumbnails(thumbnail_link, it)
	pull_metadata(metadata_link, it)
	it += 1


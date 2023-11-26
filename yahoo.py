import json
import requests
from selectolax.parser import HTMLParser

# Add in your headers/cookies
Headers = {}

def request(query, search, page):
	link ='https://buyee.jp/item/search/query/{}?sort={}&translationType=1&page={}'.format(query, search, page)
	response = requests.get(link, headers=Headers)
	html = response.content
	tree = HTMLParser(html)
	return(tree)

def buyee_scrape(query, search_type):	
	listings = {}
	
	"""
	LET'S GET SCRAPING
	
	Arguments:
	brand: string, what brand are you looking for
	page: int, how many pages do you want to scrape 
	c_rate: float, the current conversion rate for your desired currency
	search_type: int, choose type from list - [0 - newly listed, 1 - ending soon, 2 -lowest price, 3 - highest price, 4 - most popular]
	"""

	query = query.replace(' ','%20').lower() 
	
	search_list = ['new_listed','ending_soon','lowest_price','highest_price','most_pop']
	
	search_dict = {'new_listed':'end&order=d',
	 'ending_soon':'end&order=a',
	 'lowest_price':'cbids&order=a',
	 'highest_price':'cbids&order=d',
	 'most_pop':'score&ranking=popular'
	}
	
	search = search_dict[search_list[search_type]]
		
	# Get the end page
	tree = request(query, search, '1')
	try:
		nav_element = tree.css_first('nav.search_page_navi')
		a_elements = nav_element.css('a.arrow')
		last_a_element = a_elements[-1]
		
		# Extract the data-bind value
		data_bind_value = last_a_element.attributes['data-bind']
	
		second_colon_index = data_bind_value.index(':', data_bind_value.index(':') + 1)
		second_comma_index = data_bind_value.index(',', data_bind_value.index(',') + 1)
	
		end_page = data_bind_value[second_colon_index+1:second_comma_index].strip('\"')
	except:
		end_page = 1
	
	print('query "'+query+'"\n'+str(end_page)+' pages to scrape')
	
	# Skip redownloading the first page
	skip_first = True
	for count, page in enumerate(range(1, int(end_page) + 1), start=1):
		print('page',count)
		
		if skip_first:
			skip_first = False
		else:
			tree = request(query, search, page)
		
		for block_count, product_all in enumerate(tree.css('ul.auctionSearchResult'), start=1):
			for item_count, item in enumerate(product_all.css('li.itemCard'), start=1):
				
				# Append link
				try:
					url = 'https://buyee.jp/item/yahoo/auction/' + item.css('a')[0].attributes['href'].split('/')[-1]
				except:
					print("link exception")
					pass

				# Append name
				try:
					itemname = item.css('div.itemCard__itemName')[0].text().strip()
				except:
					print("name exception")
					pass

				# Append item pic link
				try:
					pic = item.css('img.hide.g-thumbnail__image')[0].attributes['data-src']
				except:
					print("pic exception")
					pass

				# Retrieve price
				try:
					price = item.css('span.g-price')[0].text()
				except:
					print("price exception")
					pass
				
				# Append info to a dictionary
				item_id = str(url).split("/")[-1].split("?")[0]
				listings[item_id] = {
					"url": str(url),
					"name": str(itemname),
					"pic": str(pic),
					"price": str(price)
				}
				
				# Printing each listing
				#print(item_id+': "'+itemname+'"')
				#print(str(block_count)+'-'+str("{:02d}".format(item_count))+': '+item_id)
	return listings

def jsonify(file_path, data):
	with open(file_path, "w") as file:
		json.dump(data, file)
	print("JSON file created successfully")

# Search query, this script is modified to scrape all pages so search type may not matter
data = buyee_scrape('笑ゥせぇるすまん DVD', 0)

# Write json
jsonify('./test.json', data)

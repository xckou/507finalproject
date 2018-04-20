from __future__ import print_function

import requests
import secret
from tkinter import *
from bs4 import BeautifulSoup as b
from bs4 import Comment as com
import json

import sqlite3
from flask import Flask, render_template, url_for
import pprint

import csv
import plotly.plotly as py

import argparse
import requests
import sys
import urllib


def params_unique_combination(baseurl, params):
	alphabetized_keys = sorted(params.keys())
	res = []
	for key in alphabetized_keys:
		res.append("{}-{}".format(key, params[key]))
	return baseurl + "_".join(res)

def make_request_from_ta(geo_code, city_name):

	CACHE_FNAME = 'tripadvisor.json'

	try:
		cache_file = open(CACHE_FNAME, 'r')
		cache_contents = cache_file.read()
		CACHE_DICTION = json.loads(cache_contents)
		cache_file.close()
	except:
		CACHE_DICTION = {}

	print('\n\n\tStart Scraping\t\n\n')

	rest_dict={}
	main_url = 'https://www.tripadvisor.com/Restaurants-g{}-{}.html'.format(geo_code, city_name)
	unique_ident = main_url
	if unique_ident in CACHE_DICTION:
		print("Getting cached data...")
		return CACHE_DICTION[unique_ident]

	else:
		print("Making a request for new data...")
		req_1 = requests.get(main_url)
		soup = b(req_1.content, 'html.parser')
		urlList = [1,30,60,90]
		accum = 0
		for page_no in urlList:

			url = 'https://www.tripadvisor.com/RestaurantSearch?Action=PAGE&geo={}&ajax=1&itags=10591&sortOrder=relevance&o=a{}&availSearchEnabled=false'.format(geo_code, page_no)
			req_2 = requests.get(url)
			soup_2 = b(req_2.content, 'html.parser')
			small_chunk = soup_2.find_all(class_ = "ui_columns is-mobile")
			# print(len(small_chunk))
			for a in range(len(small_chunk)):
			# for a in range(1):
				t = small_chunk[a].find('a', class_="property_title")
				r_name = t.text.replace('\n', '').replace('\t', '')
				# r_score =  
				r_url = 'https://www.tripadvisor.com' + t['href']
				
				t2 = small_chunk[a].find('span', class_="item price")
				if t2 != None:
					r_price = t2.text
				else:
					r_price = "None"

				t3 = small_chunk[a].find_all('a', class_="item cuisine")
				r_cuisine = []
				if t3 != None:
					for t in t3:
						r = t.text
						r_cuisine.append(r)
				else:
					r_cuisine = "None"

				t4 = small_chunk[a].find('span', class_="reviewCount")
				r_review = t4.text.replace('\n', '').replace('\t', '')

				rest_dict[accum] = {'name':r_name,'website':r_url,'price':r_price,'cuisine':r_cuisine,'reviews':r_review}
				accum += 1

	CACHE_DICTION[unique_ident]=(rest_dict)
	dumped_json_cache = json.dumps(CACHE_DICTION)
	fw = open(CACHE_FNAME,"w")
	fw.write(dumped_json_cache)
			# print(url)
	fw.close() 
	return CACHE_DICTION[unique_ident]


# ------------------------↑↑↑↑↑GET DATA FROM TRIPADVISOR↑↑↑↑↑----------------------


try:
	# For Python 3.0 and later
	from urllib.error import HTTPError
	from urllib.parse import quote
	from urllib.parse import urlencode
except ImportError:
	# Fall back to Python 2's urllib2 and urllib
	from urllib2 import HTTPError
	from urllib import quote
	from urllib import urlencode


API_KEY= secret.api_key

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  

DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Seattle, WA'
SEARCH_LIMIT = 50


def request(host, path, api_key, url_params=None):
   
	url_params = url_params or {}
	url = '{0}{1}'.format(host, quote(path.encode('utf8')))
	headers = {
		'Authorization': 'Bearer %s' % api_key,
	}

	print(u'Querying {0} ...'.format(url))

	response = requests.request('GET', url, headers=headers, params=url_params)

	return response.json()


def search(api_key, term, location):
	
	url_params = {
		'term': term.replace(' ', '+'),
		'location': location.replace(' ', '+'),
		'limit': SEARCH_LIMIT
	}
	return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
   
	business_path = BUSINESS_PATH + business_id

	return request(API_HOST, business_path, api_key)

CACHE_FNAME1 = 'yelp_resturant.json'

try:
	cache_file = open(CACHE_FNAME1, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION1 = json.loads(cache_contents)
	cache_file.close()

except:
	CACHE_DICTION1 = {}

def query_api(term, location):
   
	response = search(API_KEY, term, location)

	businesses = response.get('businesses')

	if not businesses:
		print(u'No businesses for {0} in {1} found.'.format(term, location))
		return


	for a in businesses:
		business_id = a['id']
		if business_id in CACHE_DICTION1:
			print("Getting cached data...")
			return CACHE_DICTION1

		else:

			response = get_business(API_KEY, business_id) 
			CACHE_DICTION1[business_id] = response
			# accum += 1
			dumped_json_cache = json.dumps(CACHE_DICTION1)
			fw = open(CACHE_FNAME1,"w")
			fw.write(dumped_json_cache)
		fw.close() 
	return CACHE_DICTION1

	print(u'Result for business "{0}" found:'.format(business_id))
	pprint.pprint(response, indent=2)



def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
						type=str, help='Search term (default: %(default)s)')
	parser.add_argument('-l', '--location', dest='location',
						default=DEFAULT_LOCATION, type=str,
						help='Search location (default: %(default)s)')

	input_values = parser.parse_args()

	try:
		query_api(input_values.term, input_values.location)
	except HTTPError as error:
		sys.exit(
			'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
				error.code,
				error.url,
				error.read(),
			)
		)

API_HOST2 = 'https://api.yelp.com'
SEARCH_PATH2 = '/v3/events'
BUSINESS_PATH2 = '/v3/events/' 

def request2(host, path, api_key, url_params=None):
   
	url_params = url_params or {}
	url = '{0}{1}'.format(host, quote(path.encode('utf8')))
	headers = {
		'Authorization': 'Bearer %s' % api_key,
	}
	response = requests.request('GET', url, headers=headers, params=url_params)
	return response.json()


def search2(api_key, location):
	
	url_params = {
		# 'term': term.replace(' ', '+'),
		'location': location.replace(' ', '+'),
		'limit': SEARCH_LIMIT,
		'start_date':1522540800,
		# 'end_date':1522627199
	}
	return request2(API_HOST2, SEARCH_PATH2, api_key, url_params=url_params)


def get_business2(api_key, business_id):
	business_path = BUSINESS_PATH2 + business_id

	return request2(API_HOST2, business_path, api_key)

CACHE_FNAME2 = 'yelp_event.json'

try:
	cache_file = open(CACHE_FNAME2, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION2 = json.loads(cache_contents)
	cache_file.close()

except:
	CACHE_DICTION2 = {}

def query_api2(location):
	response = search2(API_KEY, location)
	businesses = response.get('events')

	if not businesses:
		print(u'No events in {0} found.'.format(location))
		return

	for a in businesses:
		business_id = a['id']
		if business_id in CACHE_DICTION2:
			print("Getting cached data...")
			return CACHE_DICTION2

		else:
			response = get_business2(API_KEY, business_id) 
			CACHE_DICTION2[business_id] = response
		# accum += 1
			dumped_json_cache = json.dumps(CACHE_DICTION2)
			fw = open(CACHE_FNAME2,"w")
			fw.write(dumped_json_cache)
		fw.close() 
	return CACHE_DICTION2

	print(u'Result for business "{0}" found:'.format(business_id))
	pprint.pprint(response, indent=2)


def main2():
	parser = argparse.ArgumentParser()

	parser.add_argument('-l', '--location', dest='location',
						default=DEFAULT_LOCATION, type=str,
						help='Search location (default: %(default)s)')

	input_values = parser.parse_args()

	try:
		query_api2(input_values.location)
	except HTTPError as error:
		sys.exit(
			'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
				error.code,
				error.url,
				error.read(),
			)
		)



# ------------------------↑↑↑↑↑GET DATA FROM YELP↑↑↑↑↑----------------------



DBNAME = 'finalproject.db'
YELPJSON = 'yelp_resturant.json'
YELPEVENTJSON = 'yelp_event.json'
TAJSON = 'tripadvisor.json'

def create_tournament_db():

	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	statement = '''
		DROP TABLE IF EXISTS 'TripAdvisor';
	'''
	cur.execute(statement)

	statement = '''
		DROP TABLE IF EXISTS 'YelpResturant';
	'''
	cur.execute(statement)

	statement = '''
		DROP TABLE IF EXISTS 'YelpEvent';
	'''
	cur.execute(statement)

	statement = '''
	CREATE TABLE TripAdvisor(
	"Id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"Name" Text,
	"Tag" Text,
	"ReviewCount" INTEGER,
	"Price" Text,
	"Url" Text
	)
	'''
	cur.execute(statement)
	conn.commit()

	statement = '''
	CREATE TABLE YelpResturant(
	"Id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"Name" Text,
	"YelpRating" Text,
	"Phone" Text,
	"Url" Text,
	"ReviewCount" INTEGER,
	"Latitude" Real,
	"Longitude" Real
	)
	'''
	cur.execute(statement)
	conn.commit()

	statement = '''
	CREATE TABLE YelpEvent(
	"Id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"Name" Text,
	"Attending" Text,
	"Category" Text,
	"Cost" Real,
	"Latitude" Real,
	"Longitude" Real
	)
	'''
	cur.execute(statement)
	conn.commit()


	conn.close()

def populate_tournament_db():

	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	ak = open(YELPJSON, "r")
	json_read = ak.read()
	json_dic = json.loads(json_read)
	ak.close()

	for a in json_dic:
		Name = json_dic[a]["name"]
		YelpRating = json_dic[a]["rating"]
		Phone = json_dic[a]["phone"]
		ReviewCount = json_dic[a]["review_count"]
		Url = json_dic[a]["url"]
		Latitude = json_dic[a]["coordinates"]["latitude"]
		Longitude = json_dic[a]["coordinates"]["longitude"]

		# Name = json_dic["{}".format(a)]["name"]
		# YelpRating = json_dic["{}".format(a)]["rating"]
		# Phone = json_dic["{}".format(a)]["phone"]
		# ReviewCount = json_dic["{}".format(a)]["review_count"]
		# Url = json_dic["{}".format(a)]["url"]
		# Latitude = json_dic["{}".format(a)]["coordinates"]["latitude"]
		# Longitude = json_dic["{}".format(a)]["coordinates"]["longitude"]

		tuple_for_YELP = (Name,YelpRating,Phone,Url,ReviewCount,Latitude,Longitude)
	# print(tuple_for_countries)
		statement = '''
					INSERT INTO YelpResturant VALUES (NULL,?,?,?,?,?,?,?)
		'''
		cur.execute(statement,tuple_for_YELP)

	conn.commit()


	bk = open(TAJSON, "r")
	json_read = bk.read()
	json_dic = json.loads(json_read)
	bk.close()
	a = 'https://www.tripadvisor.com/Restaurants-g{}-{}.html'.format(geo_code, city_name)
	for i in range(len(json_dic[a])):
		Name = json_dic[a]["{}".format(i)]["name"]
		Tag = str(json_dic[a]["{}".format(i)]["cuisine"]).strip('[]')
		Price = json_dic[a]["{}".format(i)]["price"]
		ReviewCount = json_dic[a]["{}".format(i)]["reviews"]
		Url = json_dic[a]["{}".format(i)]["website"]

		tuple_for_TA = (Name,Tag,ReviewCount,Price,Url)
		statement = '''
					INSERT INTO TripAdvisor VALUES (NULL,?,?,?,?,?)
		'''
		cur.execute(statement,tuple_for_TA)

	conn.commit()

	ck = open(YELPEVENTJSON, "r")
	json_read = ck.read()
	json_dic = json.loads(json_read)
	ck.close()

	for a in json_dic:
		Name = json_dic[a]["name"]
		Attending = json_dic[a]["attending_count"]
		Catagory = json_dic[a]["category"]
		Cost = json_dic[a]["cost"]
		Latitude = json_dic[a]["latitude"]
		Longitude = json_dic[a]["longitude"]

		tuple_for_YE = (Name,Attending,Catagory,Cost,Latitude,Longitude)
		statement = '''
					INSERT INTO YelpEvent VALUES (NULL,?,?,?,?,?,?)
		'''
		cur.execute(statement,tuple_for_YE)

	conn.commit()
	conn.close()


# ------------------------↑↑↑↑↑CREAT DATABASE↑↑↑↑↑----------------------


class YelpResturant():
	def __init__(self, name,latitude=None,longitude=None):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude

	def __str__(self):
		return "{}:({},{})".format(self.name,self.latitude,self.longitude)

def get_yelp_resturant():
	conn = sqlite3.connect('finalproject.db')
	cur = conn.cursor()
	statement = '''
				SELECT YelpResturant.Name, YelpResturant.Latitude, YelpResturant.Longitude 
				FROM YelpResturant
				'''
	results = cur.execute(statement)
	yelp_resturant_list = []

	for row in results:
		name = row[0]
		latitude = row[1]
		longitude = row[2]

		yelp_resturant_list.append(YelpResturant(name,latitude,longitude))
	return yelp_resturant_list

def plot_yelp_resturant():
	resturants = get_yelp_resturant()
	lat_vals = []
	lon_vals = []
	text_vals = []
	for i in resturants:
		lat_vals.append(i.latitude)
		lon_vals.append(i.longitude)
		text_vals.append(i.name)

	data = [ dict(
		type = 'scattergeo',
		locationmode = 'USA-states',
		lon = lon_vals,
		lat = lat_vals,
		text = text_vals,
		mode = 'markers',
		marker = dict(
			size = 8,
			symbol = 'star',
		))]

	min_lat = 10000
	max_lat = -10000
	min_lon = 10000
	max_lon = -10000


	for str_v in lat_vals:
		v = float(str_v)
		if v < min_lat:
			min_lat = v
		if v > max_lat:
			max_lat = v
	for str_v in lon_vals:
		v = float(str_v)
		if v < min_lon:
			min_lon = v
		if v > max_lon:
			max_lon = v

	center_lat = (max_lat + min_lat) / 2
	center_lon = (max_lon + min_lon) / 2

	max_range = max(abs(max_lat - min_lat), abs(max_lon - min_lon))
	padding = max_range * 0.3
	lat_axis = [min_lat - padding, max_lat + padding]
	lon_axis = [min_lon - padding, max_lon + padding]

	layout = dict(
		title = 'Seattle Resturant<br>(Hover for names)',
		geo = dict(
			scope='usa',
			projection=dict( type='albers usa' ),
			showland = True,
			landcolor = "rgb(250, 250, 250)",
			subunitcolor = "rgb(100, 217, 217)",
			countrycolor = "rgb(217, 100, 217)",
			lataxis={'range': lat_axis},
			lonaxis={'range': lon_axis},
			center={'lat': center_lat, 'lon': center_lon},
			countrywidth = 3,
			subunitwidth = 3
			),
		)


	fig = dict(data=data, layout=layout )
	py.plot( fig, validate=False, filename='Seattle - Resturant' )

class YelpEvent():
	def __init__(self, name,latitude=None,longitude=None,attending = None):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude
		self.attending = attending

	def __str__(self):
		return "{}:({},{})".format(self.name,self.latitude,self.longitude,self.attending)

def get_yelp_event():
	conn = sqlite3.connect('finalproject.db')
	cur = conn.cursor()
	statement = '''
				SELECT YelpEvent.Name, YelpEvent.Latitude, YelpEvent.Longitude, YelpEvent.Attending 
				FROM YelpEvent
				'''
	results = cur.execute(statement)
	yelp_event_list = []

	for row in results:
		name = row[0]
		latitude = row[1]
		longitude = row[2]
		attending = row[3]

		yelp_event_list.append(YelpEvent(name,latitude,longitude,attending))
	return yelp_event_list

def plot_yelp_event():
	resturants = get_yelp_event()
	lat_vals = []
	lon_vals = []
	text_vals = []
	# text_vals2 = []
	for i in resturants:
		lat_vals.append(i.latitude)
		lon_vals.append(i.longitude)
		text_vals.append([i.name,i.attending])
		# text_vals2.append(i.attending)

	data = [ dict(
		type = 'scattergeo',
		locationmode = 'USA-states',
		lon = lon_vals,
		lat = lat_vals,
		text = text_vals,
		mode = 'markers',
		marker = dict(
			size = 8,
			symbol = 'star',
			color = 'rgb(100, 217, 217)'
		))]

	min_lat = 10000
	max_lat = -10000
	min_lon = 10000
	max_lon = -10000


	for str_v in lat_vals:
		v = float(str_v)
		if v < min_lat:
			min_lat = v
		if v > max_lat:
			max_lat = v
	for str_v in lon_vals:
		v = float(str_v)
		if v < min_lon:
			min_lon = v
		if v > max_lon:
			max_lon = v

	center_lat = (max_lat + min_lat) / 2
	center_lon = (max_lon + min_lon) / 2

	max_range = max(abs(max_lat - min_lat), abs(max_lon - min_lon))
	padding = max_range * 0.3
	lat_axis = [min_lat - padding, max_lat + padding]
	lon_axis = [min_lon - padding, max_lon + padding]

	layout = dict(
		title = 'Seattle Events<br>(Hover for names and number of attendence)',
		geo = dict(
			scope='usa',
			projection=dict( type='albers usa' ),
			showland = True,
			landcolor = "rgb(250, 250, 250)",
			subunitcolor = "rgb(100, 217, 217)",
			countrycolor = "rgb(217, 100, 217)",
			lataxis={'range': lat_axis},
			lonaxis={'range': lon_axis},
			center={'lat': center_lat, 'lon': center_lon},
			countrywidth = 3,
			subunitwidth = 3
			),
		)


	fig = dict(data=data, layout=layout )
	py.plot( fig, validate=False, filename='Seattle - Events' )

class TripAdvisor():
	def __init__(self, name, tag=None,price=None):
		self.name = name
		self.tag = tag
		self.price = price

	def __str__(self):
		return "{}:({},{})".format(self.name,self.tag,self.price)

def get_ta_resturant():
	conn = sqlite3.connect('finalproject.db')
	cur = conn.cursor()
	statement = '''
				SELECT TripAdvisor.Name, TripAdvisor.Tag, TripAdvisor.Price 
				FROM TripAdvisor
				'''
	results = cur.execute(statement)
	ta_resturant_list = []

	for row in results:
		name = row[0]
		tag = row[1]
		price = row[2]

		ta_resturant_list.append(TripAdvisor(name,tag,price))
	return ta_resturant_list



# ------------------------↑↑↑↑↑DATA PRESENT IN PLOTLY↑↑↑↑↑----------------------


app = Flask(__name__)

@app.route('/')
def index():    

	conn = sqlite3.connect('finalproject.db')
	cur = conn.cursor()
	statement = '''
				SELECT YelpEvent.Name, YelpEvent.Attending, YelpEvent.Category,YelpEvent.Cost
				FROM YelpEvent
				'''
	results = cur.execute(statement)
	yelp_event_attending_list = []
	for row in results:
		name = row[0]
		attending = row[1]
		category = row[2]
		cost = row[3]

		yelp_event_attending_list.append([name,attending,category,cost])
	return render_template('attending.html',my_list = yelp_event_attending_list)

@app.route('/tripadvisor')
def tripadvisor_view():
	conn = sqlite3.connect('finalproject.db')
	cur = conn.cursor()
	statement = '''
				SELECT TripAdvisor.Name, TripAdvisor.Tag, TripAdvisor.ReviewCount,TripAdvisor.Price,TripAdvisor.Url
				FROM TripAdvisor
				'''
	results = cur.execute(statement)
	tripadvisor_view_list = []
	for row in results:
		name = row[0]
		tag = row[1]
		reviewcount = row[2]
		price = row[3]
		url = row[4]

		tripadvisor_view_list.append([name,tag,reviewcount,price,url])
	return render_template('tripadvisor.html',my_list = tripadvisor_view_list)



@app.route('/tripadvisoryelp')
def tripadvisor_yelp():
	conn = sqlite3.connect('finalproject.db')
	cur = conn.cursor()
	statement = '''
				SELECT TripAdvisor.Name, TripAdvisor.Tag,YelpResturant.Phone,TripAdvisor.Url,YelpResturant.Url
				FROM TripAdvisor
				JOIN YelpResturant
				ON TripAdvisor.Name = YelpResturant.Name
				'''
	results = cur.execute(statement)
	tripadvisor_yelp_list = []
	for row in results:
		name = row[0]
		tag = row[1]
		phone = row[2]
		turl = row[3]
		yurl = row[4]

		tripadvisor_yelp_list.append([name,tag,phone,turl,yurl])
	return render_template('tripadvisoryelp.html',my_list = tripadvisor_yelp_list)

def run_flask():
	print('starting Flask app', app.name)  
	app.run(debug=True, use_reloader=False)

# ------------------------↑↑↑↑↑DATA PRESENT IN FLASK↑↑↑↑↑----------------------


if __name__ == '__main__':
	

	run = True
	while run == True:
		

		city_name = input("Please input the place for searching (format example:'Seattle_Washington'), 'exit' to exit: ")
		if city_name == 'Seattle_Washington':
				geo_code = 'g60878'
				make_request_from_ta(geo_code, city_name)
				main()
				main2()
				create_tournament_db()
				populate_tournament_db()
				get_ta_resturant()
				# print('starting Flask app', app.name)  
				# app.run(debug=True)


				ll = '''
			1. Plotly for distribution of Yelp Resturant
			2. Plotly for distribution of Yelp Events
			3. Flask for Details of Yelp Events
			4. Flask for Tripadvisor Resturant
			5. See which resturants show both on Yelp and Tripadvisor'''
				visual_present = input("Please choose the data options by type in a number {}, 'exit' to exit: ".format(ll))
				if visual_present == "1":
					plot_yelp_resturant()

				elif visual_present == "2":
					plot_yelp_event()

				elif visual_present == "3":
					print("Please go for http://127.0.0.1:5000/ to check the results")
					run_flask()
					
				elif visual_present == "4":
					print("Please go for http://127.0.0.1:5000/tripadvisor to check the results")
					run_flask()					

				elif visual_present == "5":
					print("Please go for http://127.0.0.1:5000/tripadvisoryelp to check the results") 
					run_flask()					
					

				elif visual_present == "exit":
					run = False

		elif city_name == "exit":
			run = False

	print("Thanks! Bye!")
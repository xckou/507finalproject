# forflask.py
import sqlite3

from flask import Flask, render_template, url_for
import pprint

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


if __name__ == '__main__':  
	print('starting Flask app', app.name)  
	app.run(debug=True)
import os
from flask import Flask, render_template, url_for, request, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import folium
from folium import plugins
import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

app = Flask(__name__)
geolocator = Nominatim(user_agent="Travel Tracker")
app.config["MONGO_DBNAME"] = 'travel_tracker'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)
countries = mongo.db.country.find()
hotels = mongo.db.hotel.find()
map_obj = folium.Map([45, 3], zoom_start=4)
plugins.LocateControl().add_to(map_obj)
plugins.Fullscreen(
    position='topright',
    title='Expand me',
    title_cancel='Exit me',
    force_separate_button=True
).add_to(map_obj)
map_obj.save('templates/travelmap.html')
url = requests.get('https://ipinfo.io/')

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/travel_planner')
def travel_planner():
    return render_template('planner.html', country=mongo.db.country.find(), hotel=mongo.db.hotel.find())

@app.route('/current_country/<country_id>', methods=['POST', 'GET'])
def current_country(country_id):
    specific_country = mongo.db.country.find_one({'_id': ObjectId(country_id)})
    specific_hotel = mongo.db.hotel.find_one({'country_name': specific_country['country_name']})
    return render_template('country.html', specific_country=specific_country, specific_hotel=specific_hotel)

@app.route('/add_country')
def add_country():
    return render_template('addcount.html', country=countries, hotel=hotels)

@app.route('/confirm_country', methods=['POST'])
def confirm_country():
    the_country = mongo.db.country
    the_hotel = mongo.db.hotel
    the_country.insert_many([
        {
            'country_name':request.form.get('country_name'),
            'travel_to_date':request.form.get('travel_to_date'),
            'travel_from_date':request.form.get('travel_from_date'),
            'flight_time_to':request.form.get('flight_time_to'),
            'flight_time_from':request.form.get('flight_time_from'),
            'todo_done':request.form.get('todo_done'),
            'blog':request.form.get('blog'),
            'rating':request.form.get('rating')
        }])
    the_hotel.insert_many([
        {
            'country_name':request.form.get('country_name'),
            'hotel_name':request.form.get('hotel_name'),
            'hotel_address':request.form.get('hotel_address'),
            'hotel_postcode':request.form.get('hotel_postcode')
        }])
    return redirect(url_for('travel_planner'))

@app.route('/edit_country/<country_id>')
def edit_country(country_id):
    specific_country = mongo.db.country.find_one({'_id': ObjectId(country_id)})
    specific_hotel = mongo.db.hotel.find_one({'country_name': specific_country['country_name']})
    return render_template('updatecount.html', specific_country=specific_country, specific_hotel=specific_hotel)

@app.route('/update_count/<country_id>', methods=['POST'])
def update_count(country_id):
    specific_country = mongo.db.country.find_one({'_id': ObjectId(country_id)})
    update_country = mongo.db.country
    update_hotel = mongo.db.hotel
    update_country.update({'_id': ObjectId(country_id)},
        {
            'country_name':request.form.get('country_name'),
            'travel_to_date':request.form.get('travel_to_date'),
            'travel_from_date':request.form.get('travel_from_date'),
            'flight_time_to':request.form.get('flight_time_to'),
            'flight_time_from':request.form.get('flight_time_from'),
            'todo_done':request.form.get('todo_done'),
            'blog':request.form.get('blog'),
            'rating':request.form.get('rating')
        })
    update_hotel.update({'country_name': specific_country['country_name']},
        {
            'country_name':request.form.get('country_name'),
            'hotel_name':request.form.get('hotel_name'),
            'hotel_address':request.form.get('hotel_address'),
            'hotel_postcode':request.form.get('hotel_postcode')
        })
    return redirect(url_for('travel_planner'))

@app.route('/delete_country/<country_id>')
def delete_country(country_id):
    specific_country = mongo.db.country.find_one({'_id': ObjectId(country_id)})
    del_country = mongo.db.country
    del_hotel = mongo.db.hotel
    del_country.remove({'_id': ObjectId(country_id)})
    del_hotel.remove({'country_name': specific_country['country_name']})
    return redirect(url_for('travel_planner'))

@app.route('/my_map')
def my_map():
    #global map_obj
    return map_obj.get_root().render()

@app.route('/travel_map')
def travel_map():
    #global map_obj

    # Adding country name from DB and adding a marker to map
    f_g = folium.FeatureGroup(name="travel_map")
    specific_country = mongo.db.country.find_one()
    for count in countries:
        d_f = pd.DataFrame({'name': count['country_name']}, index=[0])
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        d_f['location'] = d_f['name'].apply(geocode)
        d_f['point'] = d_f['location'].apply(lambda loc: tuple(loc.point) if loc else None)
        f_g.add_child(folium.Marker(location=d_f['point'][0][:-1], popup=count['country_name'], icon=folium.Icon(color='purple')))
        map_obj.add_child(f_g)
    return render_template('map.html', specific_country=specific_country)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)
import os
from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import folium
from folium import plugins
from folium.plugins import MeasureControl
import pandas

app = Flask(__name__)
app.config["SECRET_KEY"] = 'SECRET_KEY'
app.config["MONGO_DBNAME"] = 'travel_tracker'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)
countries = mongo.db.country.find()
hotels = mongo.db.hotel.find()

# Generated map
map_obj = folium.Map([45, 3], zoom_start=4, tiles="cartodbpositron")

# Locates current location
plugins.LocateControl().add_to(map_obj)

# Measure distance of points
map_obj.add_child(MeasureControl())

# Create a full screen map
plugins.Fullscreen(
    position='topright',
    title='Expand me',
    title_cancel='Exit me',
    force_separate_button=True
).add_to(map_obj)

# Adding data to map
fgc = folium.FeatureGroup(name="Top 10 countries to visit")
fgr = folium.FeatureGroup(name="Top 10 restaurants of the world")
fga = folium.FeatureGroup(name="Top 10 attractions in the world")

map_obj.add_child(fgc)
map_obj.add_child(fgr)
map_obj.add_child(fga)
map_obj.add_child(folium.LayerControl())

map_obj.save(os.path.join('templates/travelmap.html'))

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = mongo.db.user
        current_user = user.find_one({'username': request.form['username']})

        if current_user:
            session['username'] = request.form['username']
            return redirect(url_for('travel_planner'))
        flash("Username not recognised")

    if 'username' in session:
        return redirect(url_for('travel_planner'))
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = mongo.db.user
        existing_user = user.find_one({'username': request.form['username']})

        if existing_user is None:
            user.insert_one({'username': request.form['username']})
            session['username'] = request.form['username']
            return redirect(url_for('travel_planner'))
        flash("That username already exists")

    if 'username' in session:
        return redirect(url_for('travel_planner'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('travel_planner'))

@app.route('/travel_planner')
def travel_planner():
    if 'username' not in session:
        flash('Please sign in to add to your planner')
        return render_template('base.html')
    flash('Welcome ' + session['username'] + ', plan and share your journey here.')
    return render_template('planner.html', country=mongo.db.country.find(), hotel=mongo.db.hotel.find())

@app.route('/current_country/<country_id>', methods=['POST', 'GET'])
def current_country(country_id):
    specific_country = mongo.db.country.find_one({'_id': ObjectId(country_id)})
    specific_hotel = mongo.db.hotel.find_one({'country_name': specific_country['country_name']})
    return render_template('country.html', specific_country=specific_country, specific_hotel=specific_hotel)

@app.route('/add_country')
def add_country():
    return render_template('addcount.html', country=countries, hotel=hotels, rating=mongo.db.rating.find())

@app.route('/confirm_country', methods=['POST'])
def confirm_country():
    specific_user = mongo.db.user
    the_country = mongo.db.country
    the_hotel = mongo.db.hotel
    if specific_user:
        the_country.insert_many([
            {
                'username': session['username'],
                'country_name':request.form.get('country_name'),
                'travel_to_date':request.form.get('travel_to_date'),
                'travel_from_date':request.form.get('travel_from_date'),
                'flight_time_to':request.form.get('flight_time_to'),
                'flight_time_from':request.form.get('flight_time_from'),
                'todo_done':request.form.get('todo_done'),
                'blog':request.form.get('blog'),
                'rating_cat':request.form.get('rating_cat')
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
    specific_user = mongo.db.user.find_one({'username': specific_country['username']})

    if specific_user['username'] != session['username']:
        flash('You cannot edit another users post')
        return redirect(url_for('travel_planner'))
    return render_template('updatecount.html', specific_country=specific_country, specific_hotel=specific_hotel, rating=mongo.db.rating.find())

@app.route('/update_count/<country_id>', methods=['POST'])
def update_count(country_id):
    specific_country = mongo.db.country.find_one({'_id': ObjectId(country_id)})
    specific_user = mongo.db.user
    update_country = mongo.db.country
    update_hotel = mongo.db.hotel
    if specific_user:
        update_country.update({'_id': ObjectId(country_id)},
            {
                'username': session['username'],
                'country_name':request.form.get('country_name'),
                'travel_to_date':request.form.get('travel_to_date'),
                'travel_from_date':request.form.get('travel_from_date'),
                'flight_time_to':request.form.get('flight_time_to'),
                'flight_time_from':request.form.get('flight_time_from'),
                'todo_done':request.form.get('todo_done'),
                'blog':request.form.get('blog'),
                'rating_cat':request.form.get('rating_cat')
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
    specific_user = mongo.db.user.find_one({'username': specific_country['username']})
    if specific_user['username'] == session['username']:
        del_country = mongo.db.country
        del_hotel = mongo.db.hotel
        del_country.remove({'_id': ObjectId(country_id)})
        del_hotel.remove({'country_name': specific_country['country_name']})
    else:
        flash('You cannot delete another users post')
    return redirect(url_for('travel_planner'))

@app.route('/my_map')
def my_map():
    return map_obj.get_root().render()

@app.route('/travel_map')
def travel_map():
    top_count_data = pandas.read_csv('static/data/toptencount.txt')
    lat = list(top_count_data['LAT'])
    lon = list(top_count_data['LON'])
    count = list(top_count_data['COUNTRYNAME'])

    top_rest_data = pandas.read_csv('static/data/restaurants.txt')
    lati = list(top_rest_data['LAT'])
    loni = list(top_rest_data['LON'])
    countr = list(top_rest_data['COUNTRYNAME'])
    rest = list(top_rest_data['RESTAURANT'])

    top_attrac_data = pandas.read_csv('static/data/attractions.txt')
    latit = list(top_attrac_data['LAT'])
    longi = list(top_attrac_data['LON'])
    countn = list(top_attrac_data['COUNTRYNAME'])
    attrac = list(top_attrac_data['ATTRACTION'])

    for lt, ln, ct in zip(lat, lon, count):
        fgc.add_child(folium.Marker(location=(lt, ln), popup=ct, icon=folium.Icon(color='purple')))

    for lt, ln, ct, rt in zip(lati, loni, countr, rest):
        fgr.add_child(folium.Marker(location=(lt, ln), popup=rt + '\n in ' + ct, icon=folium.Icon(color='gray')))

    for lt, ln, ct, atr in zip(latit, longi, countn, attrac):
        fga.add_child(folium.Marker(location=(lt, ln), popup=atr + '\n in ' + ct, icon=folium.Icon(color='blue')))
    return render_template('map.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=False)
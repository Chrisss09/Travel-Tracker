import os
from flask import Flask, render_template, url_for, request, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'travel_tracker'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)
countries = mongo.db.country.find()
hotels = mongo.db.hotel.find()

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
    return render_template('country.html', specific_country = specific_country, specific_hotel = specific_hotel)

@app.route('/add_country')
def add_country():
    return render_template('addcount.html', country = countries, hotel = hotels)

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
    return render_template('updatecount.html', specific_country = specific_country, specific_hotel = specific_hotel)

@app.route('/update_count/<country_id>', methods=['POST'])
def update_count(country_id):
    update_country = mongo.db.country
    update_country.update_many([ {'_id': ObjectId(country_id)},
    {
        'country_name':request.form.get('country_name'),
        'travel_to_date':request.form.get('travel_to_date'),
        'travel_from_date':request.form.get('travel_from_date'),
        'flight_time_to':request.form.get('flight_time_to'),
        'flight_time_from':request.form.get('flight_time_from'),
        'todo_done':request.form.get('todo_done'),
        'blog':request.form.get('blog'),
        'rating':request.form.get('rating'),
        'hotel_name':request.form.get('hotel_name'),
        'hotel_address':request.form.get('hotel_address'),
        'hotel_postcode':request.form.get('hotel_postcode')
    }])
    return redirect(url_for('travel_planner'))
"""
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('edittask.html', task=the_task, categories=all_categories)


@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))

    <form action="{{ url_for('update_task', task_id=task._id) }}" method="POST" class="col s12">
"""


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)
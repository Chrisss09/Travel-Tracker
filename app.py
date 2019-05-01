import os
from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'travel_tracker'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)
countries = mongo.db.country.find()

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/travel_planner')
def travel_planner():
    return render_template('planner.html', country=mongo.db.country.find())

@app.route('/current_country/<country_id>', methods=['POST', 'GET'])
def current_country(country_id):
    #for count in countries.find():
        #print(count)
    specific_country = mongo.db.country.find_one({'_id': ObjectId(country_id)})
    return render_template('country.html', specific_country = specific_country)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)
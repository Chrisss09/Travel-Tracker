import os
from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'travel_tracker'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)
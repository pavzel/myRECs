import os
import random
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import env as config

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'myRecsDB'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongodb = PyMongo(app)

def find_photo_url(key, value):
    best_places = mongodb.db.myRecPlaces.find({key: value})
    best_place_images = []
    for place in best_places:
        if "photo_url" in place.keys():
            best_place_images.append(place["photo_url"])
    random.shuffle(best_place_images)
    return best_place_images

@app.route('/')
def get_places():
    places = mongodb.db.myRecPlaces.find().sort("my_opinion", -1)
    """places = mongodb.db.myRecPlaces.find({"my_opinion": { "$gte": 2} })"""
    best_place_images = find_photo_url("my_opinion", 3)
    active_tags = ["active", "", "", "", "", ""]
    return render_template('places.html', title = "All places", places = places, best_place_images = best_place_images, active_tags = active_tags)

@app.route('/place_details/<place_id>')
def place_details(place_id):
    place = mongodb.db.myRecPlaces.find_one({"_id": ObjectId(place_id)})
    active_tags = ["", "", "", "", "", ""]
    return render_template('placedetails.html', place = place, active_tags = active_tags)

@app.route('/edit_place_details/<place_id>')
def edit_place_details(place_id):
    place = mongodb.db.myRecPlaces.find_one({"_id": ObjectId(place_id)})
    active_tags = ["", "", "", "", "", ""]
    return render_template('editplacedetails.html', place = place, active_tags = active_tags)

@app.route('/update_place/<place_id>', methods=["POST"])
def update_place(place_id):
    places = mongodb.db.myRecPlaces
    my_opinion = int(request.form.get('my_opinion'))
    is_visited = bool(request.form.get('is_visited'))
    places.update_one({"_id": ObjectId(place_id)}, { "$set": {
        'place_name': request.form.get('place_name'),
        'country': request.form.get('country'),
        'my_opinion': my_opinion,
        'is_visited': is_visited,
        'website': request.form.get('website'),
        'photo_url': request.form.get('photo_url') }
    })
    return redirect(url_for('get_places'))

@app.route('/add_place')
def add_place():
    active_tags = ["", "active", "", "", "", ""]
    return render_template("addplace.html", active_tags = active_tags)

@app.route('/insert_place', methods=["POST"])
def insert_place():
    places = mongodb.db.myRecPlaces
    my_opinion = int(request.form.get('my_opinion'))
    is_visited = bool(request.form.get('is_visited'))
    places.insert_one({
        'place_name': request.form.get('place_name'),
        'country': request.form.get('country'),
        'my_opinion': my_opinion,
        'is_visited': is_visited,
        'website': request.form.get('website'),
        'photo_url': request.form.get('photo_url')
    })
    return redirect(url_for('get_places'))

@app.route('/delete_place/<place_id>')
def delete_place(place_id):
    mongodb.db.myRecPlaces.remove({'_id': ObjectId(place_id)})
    return redirect(url_for('get_places'))

@app.route('/browse')
def browse():
    """countries = ["Sweden", "Germany"]"""
    active_tags = ["", "", "active", "", "", ""]
    countries = mongodb.db.countries.find()
    return render_template("browse.html", active_tags = active_tags, countries = countries)

@app.route('/get_selested_places', methods=["POST"])
def get_selected_places():
    list_of_countries = request.form.getlist('country')
    places = mongodb.db.myRecPlaces.find({"country": { "$in": list_of_countries } })
    best_place_images = find_photo_url("my_opinion", 3)
    active_tags = ["active", "", "", "", "", ""]
    return render_template('places.html', title = "Selected places", places = places, best_place_images = best_place_images, active_tags = active_tags)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
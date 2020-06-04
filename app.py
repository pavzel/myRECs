import os
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
    return best_place_images

@app.route('/')
def get_places():
    places = mongodb.db.myRecPlaces.find()
    best_place_images = find_photo_url("my_opinion", 3)
    return render_template('places.html', places = places, best_place_images = best_place_images)

@app.route('/place_details/<place_id>')
def place_details(place_id):
    place = mongodb.db.myRecPlaces.find_one({"_id": ObjectId(place_id)})
    return render_template('placedetails.html', place = place)

@app.route('/edit_place_details/<place_id>')
def edit_place_details(place_id):
    place = mongodb.db.myRecPlaces.find_one({"_id": ObjectId(place_id)})
    return render_template('editplacedetails.html', place = place)

@app.route('/update_place/<place_id>', methods=["POST"])
def update_place(place_id):
    places = mongodb.db.myRecPlaces
    print("To update")
    print(request.form.get('place_name'))
    places.update({"_id": ObjectId(place_id)}, {
        'place_name': request.form.get('place_name')
    })
    return redirect(url_for('get_places'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
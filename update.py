import os
import math
import random
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'myRecsDB'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongodb = PyMongo(app)


@app.route('/')
def see():
    places = mongodb.db.myRecPlaces
    for place in places.find():
        new_object = {}
        place_id = place['_id']
        if not ('users' in place.keys()):
            if 'my_opinion' in place.keys():
                new_object['my_opinion'] = int(place['my_opinion'])
            else:
                new_object['my_opinion'] = int(0)
            if 'is_visited' in place.keys():
                new_object['is_visited'] = bool(place['is_visited'])
            else:
                new_object['my_opinion'] = bool(False)
            if 'photo_url' in place.keys():
                new_object['photo_url'] = place['photo_url']
            else:
                new_object['photo_url'] = ''
            if 'website' in place.keys():
                new_object['website'] = place['website']
            else:
                new_object['website'] = ''
            if 'comment' in place.keys():
                new_object['comment'] = place['comment']
            else:
                new_object['comment'] = ''
            places.update_one({"_id": ObjectId(place_id)}, { "$set": { 'users': { 'pavzel': new_object } } })
        else:
            print("No need to update!!!")

    return render_template('see.html', place = place, place_id = place_id, new_object = new_object)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)

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

params = {  "username": '',
            "countries_to_display": [],
            "nav_active_main": ["active", "", "", "", "", ""],
            "nav_active_curr": ["active", "", "", "", "", ""],
            "best_place_images": [],
            "title_to_display": "All places",
            "per_page": 15,
            "max_page": 1,
            "curr_page": 1}

def find_photo_url(value):
    best_places = mongodb.db.myRecPlaces.find({"my_opinion": { "$gte": value } })
    best_place_images = []
    for place in best_places:
        if 'photo_url' in place.keys():
            best_place_images.append(place["photo_url"])
    random.shuffle(best_place_images)
    return best_place_images

def update_countries(country):
    is_in_db = mongodb.db.countries.count_documents({"country_name": country})
    if is_in_db == 0:
        countries = mongodb.db.countries
        countries.insert_one({ 'country_name': country })

@app.route('/')
def get_all_places():
    global params
    params["nav_active_main"] = ["active", "", "", "", "", ""]
    params["title_to_display"] = "All places"
    params["curr_page"] = 1
    params["countries_to_display"].clear()
    countries = mongodb.db.countries.find().sort("country_name")
    for country in countries:
        params["countries_to_display"].append(country["country_name"])
    return redirect(url_for('display_places', page_number=1))

@app.route('/display_places/<page_number>')
def display_places(page_number):
    global params
    params["nav_active_curr"] = params["nav_active_main"]
    params["best_place_images"] = find_photo_url(2)
    number_of_places_to_display = mongodb.db.myRecPlaces.count_documents({"country": { "$in": params["countries_to_display"] } })
    params["max_page"] = math.ceil(number_of_places_to_display / params["per_page"])
    params["curr_page"] = int(page_number)
    index_min = params["per_page"] * (params["curr_page"] - 1)
    index_max = params["per_page"] * params["curr_page"]
    places = mongodb.db.myRecPlaces.find({"country": { "$in": params["countries_to_display"] } }).sort("my_opinion", -1)[index_min:index_max]
    """places = mongodb.db.myRecPlaces.find({"my_opinion": { "$gte": 2} })"""
    return render_template('places.html', places = places, params = params)

@app.route('/place_details/<place_id>')
def place_details(place_id):
    global params
    place = mongodb.db.myRecPlaces.find_one({"_id": ObjectId(place_id)})
    params["nav_active_curr"] = ["", "", "", "", "", ""]
    return render_template('placedetails.html', place = place, params = params)

@app.route('/edit_place_details/<place_id>')
def edit_place_details(place_id):
    global params
    place = mongodb.db.myRecPlaces.find_one({"_id": ObjectId(place_id)})
    params["nav_active_curr"] = ["", "", "", "", "", ""]
    return render_template('editplacedetails.html', place = place, params = params)

@app.route('/update_place/<place_id>', methods=["POST"])
def update_place(place_id):
    global params
    places = mongodb.db.myRecPlaces
    country = request.form.get('country')
    if country == '':
        country = 'not sure'
    update_countries(country)
    my_opinion = int(request.form.get('my_opinion'))
    is_visited = bool(request.form.get('is_visited'))
    places.update_one({"_id": ObjectId(place_id)}, { "$set": {
        'place_name': request.form.get('place_name'),
        'country': country,
        'my_opinion': my_opinion,
        'is_visited': is_visited,
        'website': request.form.get('website'),
        'photo_url': request.form.get('photo_url'),
        'comment': request.form.get('comment') }
    })
    return redirect(url_for('display_places', page_number=params["curr_page"]))

@app.route('/add_place')
def add_place():
    global params
    params["nav_active_curr"] = ["", "active", "", "", "", ""]
    return render_template("addplace.html", params = params)

@app.route('/insert_place', methods=["POST"])
def insert_place():
    places = mongodb.db.myRecPlaces
    country = request.form.get('country')
    if country == '':
        country = 'not sure'
    update_countries(country)
    my_opinion = int(request.form.get('my_opinion'))
    is_visited = bool(request.form.get('is_visited'))
    places.insert_one({
        'place_name': request.form.get('place_name'),
        'country': country,
        'my_opinion': my_opinion,
        'is_visited': is_visited,
        'website': request.form.get('website'),
        'photo_url': request.form.get('photo_url'),
        'comment': request.form.get('comment')
    })
    return redirect(url_for('get_all_places'))

@app.route('/delete_place/<place_id>')
def delete_place(place_id):
    mongodb.db.myRecPlaces.remove({'_id': ObjectId(place_id)})
    return redirect(url_for('display_places', page_number=params["curr_page"]))

@app.route('/search')
def search():
    global params
    params["nav_active_curr"] = ["", "", "active", "", "", ""]
    countries = mongodb.db.countries.find().sort("country_name")
    return render_template("search.html", params = params, countries = countries)

@app.route('/get_selested_places', methods=["POST"])
def get_selected_places():
    global params
    params["nav_active_main"] = ["", "", "", "", "", ""]
    params["title_to_display"] = "Selected places"
    params["curr_page"] = 1
    params["countries_to_display"] = request.form.getlist('country')
    return redirect(url_for('display_places', page_number=1))

@app.route('/login/<login_problem>')
def login(login_problem):
    global params
    params["nav_active_curr"] = ["", "", "", "", "active", ""]
    return render_template("login.html", params = params, login_problem = login_problem)

@app.route('/sign_in', methods=["POST"])
def sign_in():
    global params
    users = mongodb.db.users
    username = request.form.get('username')
    password = request.form.get('password')
    if users.count_documents({"username": username}) == 1:
        user = users.find_one({"username": username})
        if user['password'] == password:
            params['username'] = username
            return redirect(url_for('get_all_places'))
    return render_template("login.html", params = params, login_problem = True)

@app.route('/logout')
def logout():
    global params
    params['username'] = ''
    return redirect(url_for('get_all_places'))

@app.route('/sign_up/<signup_problem>')
def sign_up(signup_problem):
    global params
    params["nav_active_curr"] = ["", "", "", "", "", ""]
    return render_template("signup.html", params = params, signup_problem = signup_problem)

@app.route('/add_user')
def add_user():
    print("User is added!")
    return render_template("login.html", params = params, login_problem = False)

@app.route('/insert_user', methods=["POST"])
def insert_user():
    global params
    users = mongodb.db.users
    username = request.form.get('username')
    password = request.form.get('password')
    if users.count_documents({"username": username}) == 0 and username != '':
        users.insert_one({'username': username, 'password': password})
        return redirect(url_for('login', login_problem = False))
    return render_template("signup.html", params = params, signup_problem = True)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)

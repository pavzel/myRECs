import os
import math
import random
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


params = {  "username": '',
            "countries_to_display": [],
            "nav_active_main": ["active", "", "", "", "", ""],
            "nav_active_curr": ["active", "", "", "", "", ""],
            "best_place_images": [],
            "title_to_display": "All places",
            "per_page": 15,
            "max_page": 1,
            "curr_page": 1}

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'myRecsDB'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongodb = PyMongo(app)


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
    return render_template('places.html', places = places, params = params)


@app.route('/place_details/<place_id>')
def place_details(place_id):
    global params
    print('Logged in user:', params['username'])
    place = mongodb.db.myRecPlaces.find_one({"_id": ObjectId(place_id)})
    place_dict = {}
    for key in place:
        place_dict[key] = place[key]
    place_dict2 = {}
    place_dict2['_id'] = place_dict['_id']
    if params['username'] == '':
        place_dict2['status'] = 'anonymous'
    else:
        if params['username'] in place['users'].keys():
            place_dict2['status'] = 'contributor'
        else:
            place_dict2['status'] = 'visitor'
    place_dict2['place_name'] = place_dict['place_name']
    place_dict2['country'] = place_dict['country']
    if place_dict2['status'] == 'contributor':
        place_dict2['my_opinion'] = int(place_dict['users'][params['username']]['my_opinion'])
        place_dict2['is_visited'] = place_dict['users'][params['username']]['is_visited']
    place_dict2['opinion'] = 0
    place_dict2['opinions'] = []
    place_dict2['photo_urls'] = []
    place_dict2['websites'] = []
    place_dict2['comments'] = []
    users = place_dict['users']
    for user in users:
        place_dict2['opinion'] += int(users[user]['my_opinion'])
        place_dict2['opinions'].append(int(users[user]['my_opinion']))
        if users[user]['photo_url'] != '':
            place_dict2['photo_urls'].append(users[user]['photo_url'])
        if users[user]['website'] != '':
            place_dict2['websites'].append(users[user]['website'])
        if users[user]['comment'] != '':
            place_dict2['comments'].append(users[user]['comment'])
    place_dict2['opinion'] /= len(place_dict2['opinions'])
    if place_dict2['opinion'] > 0:
        place_dict2['opinion_str'] = '+' + str(round(place_dict2['opinion'], 2))
    else:
        place_dict2['opinion_str'] = str(round(place_dict2['opinion'], 2))
    place_dict2['opinion_int'] = int(round(place_dict2['opinion']))
    print('Place dict2:', place_dict2)
    params["nav_active_curr"] = ["", "", "", "", "", ""]
    return render_template('placedetails.html', place = place_dict2, params = params)


@app.route('/edit_place_details/<place_id>')
def edit_place_details(place_id):
    global params
    place = mongodb.db.myRecPlaces.find_one({"_id": ObjectId(place_id)})
    params["nav_active_curr"] = ["", "", "", "", "", ""]
    editor = params['username']
    if not (editor in place['users'].keys()):
        new_user = {}
        new_user['my_opinion'] = int(0)
        new_user['is_visited'] = bool(False)
        new_user['photo_url'] = ''
        new_user['website'] = ''
        new_user['comment'] = ''
        users = place['users']
        users[editor] = new_user
        places = mongodb.db.myRecPlaces
        places.update_one({"_id": ObjectId(place_id)}, {"$set": {'users': users}})
    return render_template('editplacedetails.html', place=place, params=params, editor=editor)


@app.route('/update_place/<place_id>', methods=["POST"])
def update_place(place_id):
    global params
    editor = params['username']
    places = mongodb.db.myRecPlaces
    place = places.find_one({"_id": ObjectId(place_id)})
    place_modified = {}
    place_modified['place_name'] = request.form.get('place_name')
    country = request.form.get('country')
    if country == '':
        country = 'not sure'
    update_countries(country)
    place_modified['country'] = country
    places.update_one({"_id": ObjectId(place_id)}, {"$set": place_modified})
    users = place['users']
    users[editor]['my_opinion'] = int(request.form.get('my_opinion'))
    users[editor]['is_visited'] = bool(request.form.get('is_visited'))
    users[editor]['photo_url'] = request.form.get('photo_url')
    users[editor]['website'] = request.form.get('website')
    users[editor]['comment'] = request.form.get('comment')
    places.update_one({"_id": ObjectId(place_id)}, {"$set": {'users': users}})
    return redirect(url_for('display_places', page_number=params["curr_page"]))

@app.route('/add_place')
def add_place():
    global params
    params["nav_active_curr"] = ["", "active", "", "", "", ""]
    return render_template("addplace.html", params = params)


@app.route('/insert_place', methods=["POST"])
def insert_place():
    global params
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
        'added_by': params['username'],
        'users': {
            params['username']: {
                'my_opinion': my_opinion,
                'is_visited': is_visited,
                'website': request.form.get('website'),
                'photo_url': request.form.get('photo_url'),
                'comment': request.form.get('comment')
            }
        }
    })
    return redirect(url_for('get_all_places'))


@app.route('/delete_place/<place_id>')
def delete_place(place_id):
    global params
    places = mongodb.db.myRecPlaces
    place = places.find_one({"_id": ObjectId(place_id)})
    if params['username'] == place['added_by']:
        places.remove({'_id': ObjectId(place_id)})
    else:
        users = place['users']
        users.pop(params['username'])
        places.update_one({"_id": ObjectId(place_id)}, {"$set": {'users': users}})
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

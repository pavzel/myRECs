import os
import math
import random
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


params = {  #"logged_in_user": '',
            "place_opinion": {},
            "is_rec": False,
            "countries_to_display": [],
            "nav_active_main": ["active", "", "", "", "", ""],
            "nav_active_curr": ["active", "", "", "", "", ""],
            "best_place_images": [],
            "title_to_display": "All places:",
            "per_page": 15,
            "max_page": 1,
            "curr_page": 1}

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'myRecsDB'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get("SECRET")

mongodb = PyMongo(app)


def get_photos_of_best_places(value, number):
    best_places = mongodb.db.myRecPlaces.find({"opinion": { "$gte": value } })
    best_place_images = []
    for place in best_places:
        place_photo = get_random_photo(place['users'])
        if not (place_photo is None):
            best_place_images.append(place_photo)
    random.shuffle(best_place_images)
    return best_place_images[0:number]


def update_countries(country):
    is_in_db = mongodb.db.countries.count_documents({"country_name": country})
    if is_in_db == 0:
        countries = mongodb.db.countries
        countries.insert_one({ 'country_name': country })


def calculate_users_opinion(users):
    users_opinion = 0
    users_opinions = []
    for user in users:
        users_opinion += int(users[user]['my_opinion'])
        users_opinions.append(int(users[user]['my_opinion']))
    users_opinion /= len(users_opinions)
    return users_opinion


def float_to_str_int(opinion):
    if opinion > 0:
        opinion_str = '+' + str(round(opinion, 2))
    else:
        opinion_str = str(round(opinion, 2))
    opinion_int = int(round(opinion))
    return opinion_str, opinion_int


def get_users_opinion(users):
    users_opinion = calculate_users_opinion(users)
    return float_to_str_int(users_opinion)


def get_random_photo(users):
    users_photos = []
    for user in users:
        photo_url = users[user]['photo_url']
        if photo_url != '':
            users_photos.append(users[user]['photo_url'])
    random.shuffle(users_photos)
    if len(users_photos) == 0:
        output_url = None
    else:
        output_url = users_photos[0]
    return output_url


@app.route('/')
def get_all_places():
    global params
    # Set display parameters
    params['nav_active_main'] = ["active", "", "", "", "", ""]
    params['title_to_display'] = "All places:"
    params['curr_page'] = 1
    params['is_rec'] = False
    # Prepare place_opinion dictionary
    places = mongodb.db.myRecPlaces.find()
    params['place_opinion'] = {}
    for place in places:
        params['place_opinion'][place['_id']] = place['opinion']
    return redirect(url_for('display_places', page_number=1))


@app.route('/display_places/<page_number>')
def display_places(page_number):
    global params
    # Select places to display
    place_opinion = params['place_opinion']
    # Calculate the range of documents to display
    total_number_of_places = len(place_opinion)
    params["max_page"] = math.ceil(total_number_of_places / params["per_page"])
    params["curr_page"] = int(page_number)
    index_min = params["per_page"] * (params["curr_page"] - 1)
    index_max = params["per_page"] * params["curr_page"]
    if index_max > total_number_of_places:
        index_max = index_min + total_number_of_places % params["per_page"]
    # Sorting of places according to opinion
    list_for_sorting = []
    for place in place_opinion:
        list_for_sorting.append((place, place_opinion[place]))
    list_sorted = sorted(list_for_sorting, key=lambda tuple: tuple[1], reverse=True)
    # Out of the sorted list choose only those places that must be displayed on the current page
    place_id_list = []
    for index in range(index_min, index_max):
        place_id_list.append(list_sorted[index][0])
    # Get data places that must be displayed and save them in a dictionary 
    places = mongodb.db.myRecPlaces.find({"_id": { "$in": place_id_list } })
    places_dict = {}
    for place in places:
        places_dict[place['_id']] = place
    # For the selected places, prepare a list with data essential for display
    places_list = []
    for place_id in place_id_list:
        place = places_dict[place_id]
        place_name = place['place_name']
        photo_url = get_random_photo(place['users'])
        if photo_url is None:
            photo_url = 'https://via.placeholder.com/700x400/0000FF/FFFFFF/?text=No+photo+yet'
        if params['is_rec'] is True:
            footer_text = "RECommendation:"
        else:
            footer_text = "Users' opinion:"
        opinion_str, opinion_int = float_to_str_int(place_opinion[place_id])
        places_list.append({
            '_id': place['_id'],
            'photo_url': photo_url,
            'place_name': place_name,
            'footer_text': footer_text,
            'opinion_str': opinion_str,
            'opinion_int': opinion_int
        })
    # Set display parameters
    params['nav_active_curr'] = params['nav_active_main']
    params['best_place_images'] = get_photos_of_best_places(1, 3)
    return render_template('places.html', places=places_list, params=params, session=session)


@app.route('/place_details/<place_id>')
def place_details(place_id):
    global params
    #editor = params['logged_in_user']
    if 'logged_in_user' in session:
        editor = session['logged_in_user']
    else:
        editor = ''
    place = mongodb.db.myRecPlaces.find_one({"_id": ObjectId(place_id)})
    place_dict = {}
    for key in place:
        place_dict[key] = place[key]
    place_dict2 = {}
    place_dict2['_id'] = place_dict['_id']
    if editor == '':
        place_dict2['status'] = 'anonymous'
    else:
        if editor in place['users']:
            place_dict2['status'] = 'contributor'
        else:
            place_dict2['status'] = 'visitor'
    place_dict2['place_name'] = place_dict['place_name']
    place_dict2['country'] = place_dict['country']
    if place_dict2['status'] == 'contributor':
        place_dict2['my_opinion'] = int(place_dict['users'][editor]['my_opinion'])
        place_dict2['is_visited'] = place_dict['users'][editor]['is_visited']
    place_dict2['photo_urls'] = []
    place_dict2['websites'] = []
    place_dict2['comments'] = []
    users = place_dict['users']
    for user in users:
        if users[user]['photo_url'] != '':
            place_dict2['photo_urls'].append(users[user]['photo_url'])
        if users[user]['website'] != '':
            place_dict2['websites'].append(users[user]['website'])
        if users[user]['comment'] != '':
            place_dict2['comments'].append(users[user]['comment'])
    if len(place_dict2['photo_urls']) == 0:
        place_dict2['photo_urls'] = ['https://via.placeholder.com/700x400/0000FF/FFFFFF/?text=No+photo+yet']
    place_dict2['opinion_str'], place_dict2['opinion_int'] = get_users_opinion(users)
    place_dict2['rec_str'], place_dict2['rec_int'] = float_to_str_int(params['place_opinion'][ObjectId(place_id)])
    # Set display parameters
    params['nav_active_curr'] = ["", "", "", "", "", ""]
    return render_template('placedetails.html', place = place_dict2, params = params, session=session)


@app.route('/edit_place_details/<place_id>')
def edit_place_details(place_id):
    global params
    #editor = params['logged_in_user']
    if 'logged_in_user' in session:
        editor = session['logged_in_user']
    else:
        editor = ''
    place = mongodb.db.myRecPlaces.find_one({"_id": ObjectId(place_id)})
    if not (editor in place['users']):
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
    # Set display parameters
    params['nav_active_curr'] = ["", "", "", "", "", ""]
    return render_template('editplacedetails.html', place=place, params=params, editor=editor, session=session)


@app.route('/update_place/<place_id>', methods=["POST"])
def update_place(place_id):
    global params
    #editor = params['logged_in_user']
    if 'logged_in_user' in session:
        editor = session['logged_in_user']
    else:
        editor = ''
    places = mongodb.db.myRecPlaces
    # Update user-specific data
    place = places.find_one({"_id": ObjectId(place_id)})
    users = place['users']
    users[editor]['my_opinion'] = int(request.form.get('my_opinion'))
    users[editor]['is_visited'] = bool(request.form.get('is_visited'))
    users[editor]['photo_url'] = request.form.get('photo_url')
    users[editor]['website'] = request.form.get('website')
    users[editor]['comment'] = request.form.get('comment')
    places.update_one({"_id": ObjectId(place_id)}, {"$set": {'users': users}})
    # Update general data
    place = places.find_one({"_id": ObjectId(place_id)})
    place_modified = {}
    place_modified['place_name'] = request.form.get('place_name')
    country = request.form.get('country')
    if country == '':
        country = 'not sure'
    update_countries(country)
    place_modified['country'] = country
    place_modified['opinion'] = calculate_users_opinion(users)
    places.update_one({"_id": ObjectId(place_id)}, {"$set": place_modified})

    return redirect(url_for('display_places', page_number=params["curr_page"]))


@app.route('/add_place')
def add_place():
    global params
    # Set display parameters
    params['nav_active_curr'] = ["", "active", "", "", "", ""]
    return render_template('addplace.html', params=params, session=session)


@app.route('/insert_place', methods=["POST"])
def insert_place():
    global params
    #editor = params['logged_in_user']
    if 'logged_in_user' in session:
        editor = session['logged_in_user']
    else:
        editor = ''
    places = mongodb.db.myRecPlaces
    country = request.form.get('country')
    if country == '':
        country = 'not sure'
    update_countries(country)
    opinion = float(request.form.get('my_opinion'))
    my_opinion = int(opinion)
    is_visited = bool(request.form.get('is_visited'))
    places.insert_one({
        'place_name': request.form.get('place_name'),
        'country': country,
        'added_by': editor,
        'opinion': opinion,
        'users': {
            editor: {
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
    #editor = params['logged_in_user']
    if 'logged_in_user' in session:
        editor = session['logged_in_user']
    else:
        editor = ''
    places = mongodb.db.myRecPlaces
    #Delete user's record about the place
    place = places.find_one({"_id": ObjectId(place_id)})
    if editor == place['added_by']:
        places.remove({'_id': ObjectId(place_id)})
    else:
        users = place['users']
        users.pop(editor)
        places.update_one({"_id": ObjectId(place_id)}, {"$set": {'users': users}})
        #Update users' opinion for the place
        place = places.find_one({"_id": ObjectId(place_id)})
        opinion = calculate_users_opinion(place['users'])
        places.update_one({"_id": ObjectId(place_id)}, {"$set": {'opinion': opinion}})
    return redirect(url_for('get_all_places'))


@app.route('/search')
def search():
    global params
    countries = mongodb.db.countries.find().sort("country_name")
    # Set display parameters
    params['nav_active_curr'] = ["", "", "active", "", "", ""]
    return render_template("search.html", params = params, countries = countries, session=session)


@app.route('/get_selested_places', methods=["POST"])
def get_selected_places():
    global params
    # Set display parameters
    params['nav_active_main'] = ["", "", "", "", "", ""]
    params['title_to_display'] = "Selected places:"
    params['curr_page'] = 1
    params['is_rec'] = False
    # Prepare place_opinion dictionary
    selected_countries = request.form.getlist('country')
    places = mongodb.db.myRecPlaces.find({"country": {"$in": selected_countries}})
    params['place_opinion'] = {}
    for place in places:
        params['place_opinion'][place['_id']] = place['opinion']
    return redirect(url_for('display_places', page_number=1))


@app.route('/login/<login_problem>')
def login(login_problem):
    global params
    # Set display parameters
    params['nav_active_curr'] = ["", "", "", "", "active", ""]
    return render_template("login.html", params = params, login_problem = login_problem, session=session)


@app.route('/sign_in', methods=["POST"])
def sign_in():
    global params
    users = mongodb.db.users
    username = request.form.get('username')
    password = request.form.get('password')
    if users.count_documents({'username': username}) == 1:
        user = users.find_one({'username': username})
        if user['password'] == password:
            #params['logged_in_user'] = username
            session['logged_in_user'] = username
            return redirect(url_for('get_all_places'))
    return render_template("login.html", params = params, login_problem = True, session=session)


@app.route('/logout')
def logout():
    global params
    #params['logged_in_user'] = ''
    session.pop('logged_in_user', None)
    return redirect(url_for('get_all_places'))


@app.route('/sign_up/<signup_problem>')
def sign_up(signup_problem):
    global params
    # Set display parameters
    params['nav_active_curr'] = ["", "", "", "", "active", ""]
    return render_template('signup.html', params=params, signup_problem=signup_problem, session=session)


@app.route('/insert_user', methods=["POST"])
def insert_user():
    global params
    users = mongodb.db.users
    username = request.form.get('username')
    password = request.form.get('password')
    if users.count_documents({'username': username}) == 0 and username != '':
        users.insert_one({'username': username, 'password': password})
        return redirect(url_for('login', login_problem = False))
    return render_template("signup.html", params = params, signup_problem = True, session=session)


@app.route('/help')
def help():
    global params
    # Set display parameters
    params['nav_active_curr'] = ["", "", "", "", "", "active"]
    return render_template('help.html', params=params, session=session)


@app.route('/recommend')
def recommend():
    global params
    # Extract data about all places
    place_list = []
    place_dict = {}
    places = mongodb.db.myRecPlaces.find()
    for place in places:
        place_list.append(place['_id'])
        place_dict[place['_id']] = place['users']
    # Extract data about all users
    user_list = []
    user_dict = {}
    users = mongodb.db.users.find()
    for user in users:
        user_list.append(user['username'])
        user_dict[user['username']] = {}
    # Extract relevant data about all users and all places
    for place_id in place_dict:
        users_in_place = place_dict[place_id]
        for username in user_dict:
            if username in users_in_place:
                user_in_place = users_in_place[username]
                user_dict[username][place_id] = {
                    'is_visited': user_in_place['is_visited'],
                    'opinion': user_in_place['my_opinion']
                }
    # Separate my data from the other users' data
    #my_name = params['logged_in_user']
    my_name = session['logged_in_user']
    user_list.remove(my_name)
    my_opinions = user_dict[my_name]
    user_dict.pop(my_name)
    # Calculate similarities
    similarity = {}
    for username in user_list:
        user_opinions = user_dict[username]
        coor = []
        for place in my_opinions:
            if my_opinions[place]['is_visited'] is True:
                my_opinion = my_opinions[place]['opinion']
                if place in user_opinions:
                    if user_opinions[place]['is_visited'] is True:
                        user_opinion = user_opinions[place]['opinion']
                        coor.append({'x': my_opinion, 'y': user_opinion})
        if len(coor) > 0:
            sum_d2 = 0
            for point in coor:
                sum_d2 += pow(point['x'] - point['y'], 2)
            similarity[username] = 1 - pow(sum_d2 / len(coor), 0.5) / 6
    # Find recommendations
    recs = {}
    for place in place_list:
        if (place in my_opinions) and (my_opinions[place]['is_visited'] is True):
            continue
        else:
            sum_opinions = 0
            sum_similarities = 0
            for user in similarity:
                user_opinions = user_dict[user]
                if place in user_opinions:
                    if user_opinions[place]['is_visited'] is True:
                        sum_opinions += user_opinions[place]['opinion'] * similarity[user]
                        sum_similarities += similarity[user]
            if sum_similarities > 0:
                recs[place] = round(sum_opinions / sum_similarities, 2)
    # Set display parameters
    params['nav_active_main'] = ["", "", "", "active", "", ""]
    params['title_to_display'] = "RECommended places:"
    params['curr_page'] = 1
    params['is_rec'] = True
    params['place_opinion'] = recs
    return redirect(url_for('display_places', page_number=1))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)

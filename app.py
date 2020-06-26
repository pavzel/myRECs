import os
import math
import random

from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists('env.py'):
    import env


PLACEHOLD = 'https://via.placeholder.com/700x400/0000FF/FFFFFF/?text=No+photo'


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'myRecsDB'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET')

mongodb = PyMongo(app)


def get_random_photo(users):
    """Return a random photo for a place.

    Append all URLs in a list. Shuffle. Return element 0.

    Args:
        users (dict): Data about a place saved by all users,
            a key is a user's name.

    Returns:
        A string with URL of a photo.
        None if no photo was saved for the place.

    """
    users_photos = []
    for user in users:
        photo_url = users[user]['photo_url']
        if photo_url != '':
            users_photos.append(users[user]['photo_url'])
    random.shuffle(users_photos)
    if users_photos:
        return users_photos[0]
    else:
        return None


def get_photos_of_best_places(value):
    """Returns URL of photos for 3 random places with high rating.

    Read data about 20 places with highest "opinion".
    For each of the 20 places get URL of a random photo
    and save in a list. Return 3 random URLs.

    Args:
        value (float): Only places with "opinion" greater or equal
            to "value" should be considered.

    Returns:
        A list with URLs of 3 photos.

    """
    best_places = mongodb.db.myRecPlaces.find(
        {'opinion': { '$gte': value }}).sort('opinion', -1).limit(20)
    best_place_images = []
    for place in best_places:
        place_photo = get_random_photo(place['users'])
        if place_photo is not None:
            best_place_images.append(place_photo)
    random.shuffle(best_place_images)
    return best_place_images[0:3]


def calculate_users_opinion(users):
    """From a MongoDB cursor save pairs id/opinion in a list.

    Args:
        users (dict): a dictionary from MongoDB 'myRecPlaces'
            collection with data added by all users. A key in users
            is a name of an individual user.

    Returns:
        users_opinion (float): opinion averaged over all users.

    """
    users_opinion = 0
    for user in users:
        users_opinion += int(users[user]['my_opinion'])
    users_opinion /= len(users)
    return users_opinion


def write_to_pair_list(mongodb_cursor):
    """From a MongoDB cursor save pairs id/opinion in a list.

    Args:
        mongodb_cursor (cursor): MongoDB cursor for 'myRecPlaces'
            collection with 'opinion' key.

    Returns:
        buff_list (list): [id, opinion].

    """
    buff_list = []
    for place in mongodb_cursor:
        buff_list.append((str(place['_id']), place['opinion']))
    return buff_list

#TEST!!!
def read_from_pair_list(list_of_pairs):
    """Save pairs id/opinion from a list in a dictionary.

    Args:
        list_of_pairs (list): [id, opinion].

    Returns:
        buffer_dict (dict): {"id": opinion}.

    """
    buffer_dict = {}
    for item in list_of_pairs:
        buffer_dict[item[0]] = item[1]
    return buffer_dict


def remove_from_pair_list(list_of_pairs, value0):
    """Remove a pair id/opinion from a list.

    Args:
        list_of_pairs (list): [id, opinion],
        value0 (str): id value in the target pair.

    Returns:
        list_of_pairs (list): a list without the target pair.

    """
    index = 0
    for item in list_of_pairs:
        if item[0] == value0:
            list_of_pairs.pop(index)
            break
        index += 1
    return list_of_pairs


def update_pair_in_list(list_of_pairs, value0, value1):
    """Update a pair id/opinion in a list.

    Args:
        list_of_pairs (list): [id, opinion],
        value0 (str): id value in the target pair,
        value1 (float): new opinion value in the target pair.

    Returns:
        list_of_pairs (list): the updated list.

    """
    index = 0
    for item in list_of_pairs:
        if item[0] == value0:
            list_of_pairs[index] = (value0, value1)
            break
        index += 1
    return list_of_pairs


def get_page_params(total_number_of_places, page):
    """Calculate parameters for pagination.

    Args:
        total_number_of_places (int): number of places on all pages,
        page (int): number of the page to be displayed.

    Returns:
        cur_page (int): new value for the current page,
        max_page (int): the maximal page number,
        index_min (int): the lower index in the place list,
        index_max (int): the upper index in the place list.

    """
    PER_PAGE = 15
    max_page = math.ceil(total_number_of_places / PER_PAGE)
    curr_page = max_page if int(page) > max_page else int(page)
    index_min = PER_PAGE * (curr_page - 1)
    index_max = PER_PAGE * curr_page
    if index_max > total_number_of_places:
        index_max = index_min + total_number_of_places % PER_PAGE
    return curr_page, max_page, index_min, index_max


def get_id_op_list(all_id_op, index_min, index_max):
    """For places to display, prepare list of IDs "id_list".

    Args:
        all_id_op (list): [id, opinion] for places on all pages,
        index_min (int): the lower index in the place list,
        index_max (int): the upper index in the place list.

    Returns:
        List of pairs [id, opinion] for the current page.

    """
    list_sorted = sorted(all_id_op, key=lambda tuple: tuple[1], reverse=True)
    return list_sorted[index_min:index_max]


def float_to_str_int(opinion):
    """Convert float to a pait of str and int.

    Form a list of IDs. For the list collect data from MongoDB
    myRecPlaces collection. Form the output list.

    Args:
        opinion (float): opinion for a place.

    Returns:
        opinion_str (str): opinion with a sign and 2 decimals,
        opinion_int (int): integer for conversion to thumbs up/down.

    """
    if opinion > 0:
        opinion_str = '+' + str(round(opinion, 2))
    else:
        opinion_str = str(round(opinion, 2))
    opinion_int = int(round(opinion))
    return opinion_str, opinion_int


def prepare_display_list(id_op_list, is_rec):
    """For places to display, repare a list with essential data.

    Form a list of IDs. For the list collect data from MongoDB
    myRecPlaces collection. Form the output list.

    Args:
        id_op_list (list): [id, opinion] for the current page,
        is_rec (bool): flag if places are REComended.

    Returns:
        display_list (list): places with data for display.

    """
    object_id_list = []
    for pair in id_op_list:
        object_id_list.append(ObjectId(pair[0]))

    places = mongodb.db.myRecPlaces.find({'_id': {'$in': object_id_list}})
    places_dict = {}
    for place in places:
        places_dict[str(place['_id'])] = place

    display_list = []
    for pair in id_op_list:
        place = places_dict[pair[0]]
        photo_url = get_random_photo(place['users'])
        if photo_url is None:
            photo_url = PLACEHOLD
        opinion_str, opinion_int = float_to_str_int(pair[1])
        display_list.append({
            '_id': place['_id'],
            'photo_url': photo_url,
            'place_name': place['place_name'],
            'footer_text': "REC-opinion:" if is_rec else "Users' opinion:",
            'opinion_str': opinion_str,
            'opinion_int': opinion_int
        })
    return display_list


def update_countries(country):
    """Update "countries" collection if necessary.

    Check if a country is in the MongoDB "countries" collection.
    If not then add it.

    Args:
        country (str): country name.

    """
    is_in_db = mongodb.db.countries.count_documents({'country_name': country})
    if is_in_db == 0:
        countries = mongodb.db.countries
        countries.insert_one({ 'country_name': country })


@app.route('/')
def get_all_places():
    """ Prepare list of all places. """
    places = mongodb.db.myRecPlaces.find({}, {'opinion': 1})
    session['id_opinion_s'] = write_to_pair_list(places)

    """ Redirect to display all places. """
    session['nav_main'] = ['active', '', '', '', '', '']
    session['title'] = 'All places:'
    session['curr_page'] = 1
    session['is_rec'] = False
    return redirect(url_for('display_many', page=session['curr_page']))


@app.route('/places/<page>')
def display_many(page):
    session['curr_page'], max_page, index_min, index_max = get_page_params(
        len(session['id_opinion_s']), page)
    id_op_list = get_id_op_list(session['id_opinion_s'], index_min, index_max)
    display_list = prepare_display_list(id_op_list, session['is_rec'])

    """ Display many places. """
    session['nav_curr'] = session['nav_main']
    return render_template(
        'places.html',
        places=display_list,
        max_page=max_page,
        head_imgs=get_photos_of_best_places(1),
        session=session)


@app.route('/place/<place_id>')
def display_one(place_id):
    place_id = str(place_id)

    """ Check if user is logged in ("editor"). """
    editor = session['loggedin_usr'] if 'loggedin_usr' in session else None

    # Get data about a place
    place = mongodb.db.myRecPlaces.find_one({'_id': ObjectId(place_id)})
    # Save data in a dictionary
    place_dict = {}
    for key in place:
        place_dict[key] = place[key]
    # Compose a dictionary with data for display
    dict2 = {}
    dict2['_id'] = place_dict['_id']
    if editor is not None:
        if editor in place['users']:
            dict2['status'] = 'contributor'
        else:
            dict2['status'] = 'visitor'
    else:
        dict2['status'] = 'anonymous'
    dict2['place_name'] = place_dict['place_name']
    dict2['country'] = place_dict['country']
    if dict2['status'] == 'contributor':
        dict2['my_opinion'] = int(
            place_dict['users'][editor]['my_opinion'])
        dict2['is_visited'] = place_dict['users'][editor]['is_visited']
    # Collect photos, websites and comment added by all users
    dict2['photo_urls'] = []
    dict2['websites'] = []
    dict2['comments'] = []
    users = place_dict['users']
    for user in users:
        if users[user]['photo_url'] != '':
            dict2['photo_urls'].append(users[user]['photo_url'])
        if users[user]['website'] != '':
            dict2['websites'].append(users[user]['website'])
        if users[user]['comment'] != '':
            dict2['comments'].append(users[user]['comment'])
    # If there is no photo yet, add a placeholder
    if not dict2['photo_urls']:
        dict2['photo_urls'] = [PLACEHOLD]
    # Add users' opinion
    dict2['opinion_str'], dict2['opinion_int'] = float_to_str_int(
        calculate_users_opinion(users))
    # If the place is RECommended then add REC-opinion to "place" dictionary
    if session['is_rec']:
        place_opinion = read_from_pair_list(session['id_opinion_s'])
        rec_opinion = place_opinion[place_id]
        dict2['rec_str'], dict2['rec_int'] = float_to_str_int(rec_opinion)

    """ Display details of one place. """
    session['nav_curr'] = ['', '', '', '', '', '']
    return render_template('place.html', place=dict2, session=session)


@app.route('/edit_place/<place_id>')
def edit_place(place_id):
    """ Check if user is logged in ("editor"). """
    if 'loggedin_usr' in session:
        editor = session['loggedin_usr']
    else:
        return redirect(url_for('login', login_problem=False))

    place = mongodb.db.myRecPlaces.find_one({'_id': ObjectId(place_id)})
    """ If no data added by the user before then initialize. """
    if not (editor in place['users']):
        is_new = True
        new_user = {}
        new_user['my_opinion'] = int(0)
        new_user['is_visited'] = bool(False)
        new_user['photo_url'] = ''
        new_user['website'] = ''
        new_user['comment'] = ''
        users = place['users']
        users[editor] = new_user
        places = mongodb.db.myRecPlaces
        places.update_one(
            {'_id': ObjectId(place_id)},
            {'$set': {'users': users}})
    else:
        is_new = False

    """ Display a form for editing details of one place. """
    session['nav_curr'] = ['', '', '', '', '', '']
    return render_template(
        'editplace.html',
        place=place,
        editor=editor,
        is_new=is_new,
        session=session)


@app.route('/update_place/<place_id>', methods=['POST'])
def update_place(place_id):
    """ Check if user is logged in ("editor"). """
    if 'loggedin_usr' in session:
        editor = session['loggedin_usr']
    else:
        return redirect(url_for('login', login_problem=False))

    places = mongodb.db.myRecPlaces
    """ Update user-specific data. """
    place = places.find_one({'_id': ObjectId(place_id)})
    users = place['users']
    users[editor] = {
        'my_opinion': int(request.form.get('my_opinion')),
        'is_visited': bool(request.form.get('is_visited')),
        'photo_url': request.form.get('photo_url'),
        'website': request.form.get('website'),
        'comment': request.form.get('comment')
    }
    places.update_one(
        {'_id': ObjectId(place_id)},
        {'$set': {'users': users}})

    """ Update general data. """
    country = request.form.get('country')
    opinion = calculate_users_opinion(users)
    places.update_one(
        {'_id': ObjectId(place_id)},
        {'$set': {
            'place_name': request.form.get('place_name'),
            'country': country,
            'opinion': opinion}
        })

    """ Update "countries" collection if necessary. """
    update_countries(country)

    """ Redirect to display places. """
    if session['title'] != 'RECommended places:':
        session['id_opinion_s'] = update_pair_in_list(
            session['id_opinion_s'], place_id, opinion)
    return redirect(url_for('display_many', page=session['curr_page']))


@app.route('/add_place')
def add_place():
    """ Display a form for adding a new place. """
    session['nav_curr'] = ['', 'active', '', '', '', '']
    return render_template('addplace.html', session=session)


@app.route('/insert_place', methods=['POST'])
def insert_place():
    """ Check if user is logged in ("editor"). """
    if 'loggedin_usr' in session:
        editor = session['loggedin_usr']
    else:
        return redirect(url_for('login', login_problem=False))

    """ Save data from form as new place. """
    country = request.form.get('country')
    opinion = float(request.form.get('my_opinion'))
    my_opinion = int(opinion)
    is_visited = bool(request.form.get('is_visited'))
    mongodb.db.myRecPlaces.insert_one({
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

    """ Update "countries" collection if necessary. """
    update_countries(country)

    """ Redirect to display places. """
    return redirect(url_for('get_all_places'))


@app.route('/delete_place/<place_id>')
def delete_place(place_id):
    """ Check if user is logged in ("editor"). """
    if 'loggedin_usr' in session:
        editor = session['loggedin_usr']
    else:
        return redirect(url_for('login', login_problem=False))

    """ Delete user's record about the place. """
    places = mongodb.db.myRecPlaces
    place = places.find_one({'_id': ObjectId(place_id)})
    if editor == place['added_by']:
        """ Delete the record form collection completely. """
        places.delete_one({'_id': ObjectId(place_id)})
        session['id_opinion_s'] = remove_from_pair_list(
            session['id_opinion_s'], place_id)
    else:
        """ Delete only data about the place added by editor. """
        users = place['users']
        users.pop(editor)
        places.update_one(
            {'_id': ObjectId(place_id)},
            {'$set': {'users': users}})
        """ Update users' opinion for the place. """
        place = places.find_one({'_id': ObjectId(place_id)})
        opinion = calculate_users_opinion(place['users'])
        places.update_one(
            {'_id': ObjectId(place_id)},
            {'$set': {'opinion': opinion}})
        session['id_opinion_s'] = update_pair_in_list(
            session['id_opinion_s'], place_id, opinion)

    """ Redirect to display places. """
    return redirect(url_for('display_many', page=session['curr_page']))


@app.route('/select')
def select():
    countries = mongodb.db.countries.find().sort('country_name')
    session['nav_curr'] = ['', '', 'active', '', '', '']
    return render_template(
        'select.html',
        countries=countries,
        session=session)


@app.route('/get_selested_places', methods=['POST'])
def get_selected_places():
    """ Prepare list of places for selected countries. """
    selected_countries = request.form.getlist('country')
    places = mongodb.db.myRecPlaces.find(
        {'country': {'$in': selected_countries}},
        {'opinion': 1})
    session['id_opinion_s'] = write_to_pair_list(places)

    """ Redirect to display selected places. """
    session['nav_main'] = ['', '', 'active', '', '', '']
    session['title'] = 'Selected places:'
    session['curr_page'] = 1
    session['is_rec'] = False
    return redirect(url_for('display_many', page=1))


@app.route('/recommend')
def recommend():
    """ Check if user is logged in ("editor"). """
    if 'loggedin_usr' in session:
        editor = session['loggedin_usr']
    else:
        return redirect(url_for('login', login_problem=False))

    """ Save data about all places in "place_dict" dictionary. """
    place_dict = {}
    places = mongodb.db.myRecPlaces.find({}, {'users': 1})
    for place in places:
        place_dict[place['_id']] = place['users']

    """ Prepare "user_dict" for opinions of individual users. """
    user_dict = {}
    users = mongodb.db.users.find({}, {'username': 1})
    for user in users:
        user_dict[user['username']] = {}

    """
    For each user save 'is_visited' and 'my_opinion' in "user_dict".
    """
    for place in place_dict:
        users_in_place = place_dict[place]
        for user in user_dict:
            if user in users_in_place:
                user_in_place = users_in_place[user]
                user_dict[user][place] = {
                    'is_visited': user_in_place['is_visited'],
                    'opinion': user_in_place['my_opinion']
                }

    """ Separate editor's data from the other users' data """
    my_opinions = user_dict[editor]
    user_dict.pop(editor)

    """ Calculate similarities. """
    similarity = {}
    for user in user_dict:
        user_opinions = user_dict[user]
        opinions_to_compare = []
        for place in my_opinions:
            if my_opinions[place]['is_visited']:
                my_opinion = my_opinions[place]['opinion']
                if place in user_opinions:
                    if user_opinions[place]['is_visited']:
                        user_opinion = user_opinions[place]['opinion']
                        opinions_to_compare.append(
                            {'my': my_opinion, 'other': user_opinion})
        if opinions_to_compare:
            sum_d2 = 0
            for opinion_pair in opinions_to_compare:
                sum_d2 += pow(opinion_pair['my'] - opinion_pair['other'], 2)
            similarity[user] = 1 - pow(sum_d2
                                       / len(opinions_to_compare), 0.5) / 6

    """ Prepare list of RECommended places with REC-opinions. """
    session['id_opinion_s'] = []
    for place in place_dict:
        if (place in my_opinions) and my_opinions[place]['is_visited']:
            continue
        else:
            sum_opinions = 0
            sum_similarities = 0
            for user in similarity:
                user_opinions = user_dict[user]
                if place in user_opinions:
                    if user_opinions[place]['is_visited']:
                        sum_opinions += (user_opinions[place]['opinion']
                                         * similarity[user])
                        sum_similarities += similarity[user]
            if sum_similarities > 0:
                session['id_opinion_s'].append(
                    (str(place), round(sum_opinions / sum_similarities, 2)))

    """ Redirect to display RECommended places if any, or all. """
    if session['id_opinion_s']:
        session['nav_main'] = ['', '', '', 'active', '', '']
        session['title'] = 'RECommended places:'
        session['curr_page'] = 1
        session['is_rec'] = True
        return redirect(url_for('display_many', page=1))
    else:
        return redirect(url_for('get_all_places'))


@app.route('/login/<login_problem>')
def login(login_problem):
    """ Display a form for log in. """
    session['nav_curr'] = ['', '', '', '', 'active', '']
    return render_template(
        'login.html',
        login_problem=login_problem,
        session=session)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    """ Get login data from form. """
    username = request.form.get('username')
    password = request.form.get('password')

    """ If username and password are valid then sign in. """
    users = mongodb.db.users
    if users.count_documents({'username': username}) == 1:
        user = users.find_one({'username': username})
        if user['password'] == password:
            session['loggedin_usr'] = username
            return redirect(url_for('get_all_places'))

    """ If problems with sign in then inform and try again. """
    return render_template(
        'login.html',
        login_problem=True,
        session=session)


@app.route('/logout')
def logout():
    session.pop('loggedin_usr', None)
    return redirect(url_for('get_all_places'))


@app.route('/sign_up/<signup_problem>')
def sign_up(signup_problem):
    """ Display a form for sign up. """
    session['nav_curr'] = ['', '', '', '', 'active', '']
    return render_template(
        'signup.html',
        signup_problem=signup_problem,
        session=session)


@app.route('/insert_user', methods=['POST'])
def insert_user():
    """ Get user's data from form. """
    username = request.form.get('username')
    password = request.form.get('password')

    """ If username is valid then redirect to sign in. """
    users = mongodb.db.users
    if users.count_documents({'username': username}) == 0:
        users.insert_one({'username': username, 'password': password})
        return redirect(url_for('login', login_problem=False))

    """ If problems with sign up then inform and try again. """
    return render_template(
        'signup.html',
        signup_problem=True,
        session=session)


@app.route('/help')
def help():
    """ Display Help Page. """
    session['nav_curr'] = ['', '', '', '', '', 'active']
    return render_template('help.html', session=session)


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP'),
        port=os.environ.get('PORT'),
        debug=True)

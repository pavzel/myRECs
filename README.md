### author: Pavel Zelenin
### Code Institute
### Full Stack Web Developer course
## Milestone Project #3
### (Practical Python and Data-Centric Development)
 
# Recommendation site myRECs

https://my-recs.herokuapp.com/


## Overview
The main purpose of this project (Milestone Project #3) was to build a full-stack site that allows users to manage a common dataset about a particular domain.
The site demonstrates some of my knowledge and skills in Python, Flask, MongoDB, and Heroku in June 2020.

This site is for me and any other person who likes traveling by car. A car provides flexibility in terms of where and when to go, to stay for a night, what to visit, and how much time to spend for a visit. Travel results in memories that can be stored and shared together with personal opinions and recommendations. Thus a user can refresh own memories and get recommendations about new places to visit from other users.

All recommendations are place-centered. A place can have just one interesting site (like Mont-Saint-Michel) or hundreds of them (like Paris) but if these sites can be reached on foot or by car within 5-20 minutes, all of them are considered to be located in the same place.

For each place the following information is saved: name, country, personal opinion ("rating", details see below), a marker (visited or not visited), a link to a photo (optional), a link to a website (optional).

A place is rated by a user according to a scale:\
    -3 means "never go there"\
    -2 means "uninteresting and unfriendly"\
    -1 means "boring"\
     0 means "rather nice but nothing special"\
    +1 means "interesting or especially nice"\
    +2 means "very interesting"\
    +3 means "outstanding/unique"\
A user can see own opinion ("my opinion"; if there is any) and "Users' opinion" based on opinions of all users. Potentially, a custom "REC -opinion" based on similarity of tastes of a user with the other users, can be calculated for places not yet visited by the user.


## UX
(TO BE ADDED)

## Features
### Existing Features
The site includes pages: Home, Place details, Editing of place details, Adding a new place, Selecting places, Recommended places, Login, and Help.\
Most of them are directly accessible via a menu. The menu is present on top of all pages, as well as a footer on bottom of all pages.
Besides these standard top menu and bottom footer different pages contain the following.

#### Home page
(accessible by clicking "Home" in menu or "myRECs" logo in the top left corner):
1. A carousel with 3 images randomly chosen from all images saved for places with "Users' opinion" higher than +1.
2. A page title "All places:".
3. Cards for not more than 15 places. Each card displays (i) a random image saved for the place, (ii) name of the place, (iii) "Details" button than leads to Place details page for the place, (iv) "Users' opinion".
4. Pagination buttons for access to all places if number of places in the set is greater than 15. "First" button brings directly to the first page. "Last" button displays the last page number and brings directly to the last page. Middle "button" just indicates the current page number. "Previous" reduces the current page number by 1. "Next" increases the current page number by 1. A button is active only if clicking it can change the current page (e.g. if the current page is the last one then "Next" and "Last" buttons are inactive).

#### Place details
(accessible by clicking "Details" button, or place photo, or place name on a place card):
1. A carousel with all images saved by all users for the place.
2. The place name.
3. User's own opinion ("my opinion") about the place if it exists and the user is logged in.
4. The place country.
5. Whether the place is visited if the user added this information and is logged in.
6. A list (if not empty) of links to websites about the place added by all users.
7. Buttons "Back" to return to the main (Home) page and "Edit" to get to Editing of place details page.
8. A list (if not empty) of comments about the place added by all users.


#### Help page
(accessible by clicking "Help" in menu):
1. basic concepts of the site,
2. instructions for users,
3. contact address for complaints, suggestions, etc.


### Features Left to Implement:
At the moment, a minimal usable version of the site is deployed. If there are many enough users interested in the site, many aspects can be imporved, for example:
1. For each place several names can be used (e.g. names in different languages). When a user wants to add a new place the place's name is compared with place names in the database and one or several names (like Syracuse in Italy, Syracuse in NY, Syracuse in IN, etc.) of already saved places are prompted.
2. Each user can add unlimited number of photos, website links and comments.
3. For each place, its geographic coordinates and position on map can be added.
4. Each item (photo, website, comment) can be rated by users. And these ratings can be used for calculation of REC-opinion.
5. Parameters other than country name (e.g. parts of place name, range of Users' opinion, number of users who visited the place etc.) can be used for filtering place sets.
6. Standard sign up and log in (with email address) can be implemented so that a user can change her/his username, password, get new password to replace the forgotten one etc.
Also the site's functionality can be expanded:
1. A trip planner can be added. A user sets departure and arrival places, total number of trip days, minimal and maximal distances for a day trip, etc. Based on these data, the site recommends possible routes with places to visit and estimates of time to spend for the visits.
2. Other services (like sites of travel agencies, hotels or museums) can be added to such a planner.


## Technologies Used
The project was written with HTML5, CSS3, Javascript, Pyhton3, Flask, MongoDB. \
[Bootstrap] toolkit (https://getbootstrap.com/) was used for simple and clear design.


## Testing
The site was designed to be used mainly on mobile phones with a small display. \
It was tested on a laptop Lenovo ThinkPad (with different window widths from 330px to 1466px) and a mobile phone Motorola XT1941 4.


## Deployment
The project is deployed to Heroku (built from the master branch): \
https://myRecs.herokuapp.com/ \
The source files are publicly accessible:\
https://github.com/pavzel/myRecs \
To run locally, you can clone this repository: paste `git clone https://github.com/pavzel/myRecs.git` into your terminal. To cut ties with this GitHub repository, type `git remote rm origin` into the terminal.
Private configuration variables (the link MONGO_URI that gives access to the MongoDB database, and the secret key SECRET used by Flask app) are not revealed.


## Credits
The photos saved in the database for this project are only from open sources like Wikipedia etc. \
The links saved in the database for this project are to open resources like Wikipedia, museum sites etc. \
The project idea was suggested by Code Institute. \
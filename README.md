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
    &emsp;0 means "rather nice but nothing special"\
    +1 means "interesting or especially nice"\
    +2 means "very interesting"\
    +3 means "outstanding/unique"\
A user can see own opinion ("my opinion"; if there is any) and "Users' opinion" based on opinions of all users. Potentially, a custom "REC -opinion" based on similarity of tastes of a user with the other users, can be calculated for places not yet visited by the user.


## UX
Use this section to provide insight into your UX process, focusing on who this website is for, what it is that they want to achieve and how your project is the best way to help them achieve these things.

In particular, as part of this section we recommend that you provide a list of User Stories, with the following general structure:

As a user type, I want to perform an action, so that I can achieve a goal.


## UX
At the moment, the site was supposed to be used by me, my friends, and maybe friends of friends. That is why its design is minimal and includes only essential feratures.
### User stories:
#### Always visible "Navigation menu"
* As a user, I want to click an always visible Home button, so that I can come back to the landing page with all places saved in the database accessible.
* As a user, I want to click an always visible Add place button, so that I can add a new place to the database.
* As a user, I want to be redirected to Login page if I click Add place button before I logged in, so that I can log in.
* As a user, I want to click an always visible Select button, so that I can select countries of interest.
* As a user, I want to click an always visible RECommend button, so that I can get personalized recommendations about the places that I haven't visited yet.
* As a user, I want to be redirected to Login page if I click RECommend button before I logged in, so that I can log in.
* As a user, I want to click an always visible Login button, so that I can log in. After successful logging in, this button must turn into Logout button with my username indicated.
* As a user, when I'm logged in I want to click an always visible Logout button, so that I can logged out. After successful logging out, this button must turn into Login button.
* As a user, I want to click an always visible Help button, so that I can get help.
#### Image carousel on the main page
* As a user, I want to see a carousel with several randomly chosen images of places with high rating, so that I can get some impression what exists in the database.
#### Place cards on the main page
* As a user, for each individual place card, I want to click Details button, or the place photo, or the place name, so that I can view information about this place added by all users.
#### Pagination buttons on the main page bottom
* As a user, I want to see my current page number, so that I know where I am.
* As a user, I want to see the last page number, so that I know how many pages this set of places includes.
* As a user, if I'm not on the first page, I want to click an always visible First button, so that I get to the first page.
* As a user, if I'm not on the first page, I want to click an always visible Previous button, so that I get to the previous page (a page with the current number decreased by 1).
* As a user, if I'm not on the last page, I want to click an always visible Next button, so that I get to the next page (a page with the current number increased by 1).
* As a user, if I'm not on the last page, I want to click an always visible Last button, so that I get to the last page.
#### Place details page
* As a user, I want to view information about the place added by all users, so that I can refresh my memories about the place or/and find out something new about it.
* As a user, I want to click Back button, so that I can return to the view with many place cards displayed from where I came to Place details.
* As a user, I want to click Edit button, so that I can get access to editing information about the place (if I added it before) or to add it (if I saved nothing previously).
* As a user, I want to be redirected to Login page if I click Edit button before I logged in, so that I can log in.
#### Editing of place details page
* As a user, I want to view and change information about the place, so that I can save it.
* As a user, I want to click Update button, so that my changed information is saved and I can return to the page with many place cards from where I came.
* As a user, I want to click Cancel button, so that I can discard all changes and return to the page with many place cards from where I came.
* As a user, I want to click Delete button, so that I can delete all information about the place added by me and return to the page with many place cards from where I came.
#### Adding a new place page
* As a user, I want to add information about the place, so that I can save it.
* As a user, I want to click Add New Place button, so that my information is saved and I can return to the page with many place cards from where I came.
* As a user, I want to click Cancel button, so that I can discard all information and return to the page with many place cards from where I came.
#### Selecting places page
* As a user, I want to select one or several countries from a list of all countries, so that I can view only places from those countries.
* As a user, I want to click Find Places button, so that I can return to the view with place cards from the selected countries displayed.
* As a user, I want to click Cancel button, so that I can discard my selection and return to the page with many place cards from where I came.
#### Recommended places page
* As a user, I want to see REC-opinion on place cards, so that I know a personalized estimate of my opinion about places that I haven't visited yet.
#### Place details page navigated from Recommended places page
* As a user, besides the standard place information, I want to see REC-opinion, so that I know a personalized estimate of my opinion the place that I haven't visited yet.
#### Login page
* As a user, I want to enter my username and password, so that I can login.
* As a user, I want to click Login button, so that my credentials are controlled I can get to Home page.
* As a user, if there is any problem with login I want to get a warning message and return to Login page, so that I can retry logging in.
* As a user, I want to click Cancel button, so that log in is cancelled and I can get to the page I came from.
* As a user, I want to click Sign Up button, so that I can get to Signup page.
#### Signup page
* As a user, I want to enter my new username and password, so that I can login in the future.
* As a user, I want to click Sign Up button, so that my credentials are controlled, saved, and I can get to Login page.
* As a user, if there is any problem with sign-up I want to get a warning message and return to Sign Up page, so that I can retry signing up.
* As a user, I want to click Cancel button, so that log in is cancelled and I can get to the page I came from.


## Features
### Existing Features
The site includes pages: Home, Place details, Editing of place details, Adding a new place, Selecting places, Selected places, Recommended places, Login, Signup and Help.\
Most of these pages are directly accessible via a menu. The menu is present on top of all pages, as well as a footer on bottom of all pages.
Besides these standard top menu and bottom footer, different pages contain the following.

#### Home
(accessible by clicking "Home" in menu or "myRECs" logo in the top left corner)
1. A carousel with 3 images randomly chosen from all images saved for places with "Users' opinion" higher than +1.
2. The page title "All places".
3. Cards for not more than 15 places. Each card displays (i) a random image saved for the place, (ii) name of the place, (iii) "Details" button than leads to Place details page for the place, (iv) "Users' opinion".
4. Pagination buttons for access to all places if number of places in the set is greater than 15. "First" button brings directly to the first page. "Last" button displays the last page number and brings directly to the last page. Middle "button" just indicates the current page number. "Previous" reduces the current page number by 1. "Next" increases the current page number by 1. A button is active only if clicking it can change the current page (e.g. if the current page is the last one then "Next" and "Last" buttons are inactive).

#### Place details
(accessible by clicking "Details" button, or place photo, or place name on a place card)
1. A carousel with all images saved by all users for the place.
2. The place name.
3. User's own opinion ("my opinion") about the place if it exists and the user is logged in.
4. The place country.
5. Whether the place is visited if the user added this information and is logged in.
6. A list (if not empty) of links to websites about the place added by all users.
7. Buttons "Back" to return to the main (Home) page and "Edit" to get to Editing of place details page.
8. A list (if not empty) of comments about the place added by all users.

#### Editing of place details
(accessible by clicking "Edit" button on Place details page, see above\
only if the user is logged in, otherwise the user is redirected to Log in page)
1. An image saved by the user for the place or a placeholder if no image was saved.
2. A text field for the place name. It can be edited only if the user added the place as a new place. This option is just for correction of misprints.
3. A slider for setting the user's own opinion ("my opinion") about the place (if the user never added information about the place then by default 0).
4. A text field for the country name. It can be edited only if the user added the place as a new place. This option is just for correction of misprints.
5. A switch to indicate whether the place is visited (by default "No").
6. A text field (optional) for a link to a website about the place.
7. A text field (optional) for a link to a place image.
8. Buttons "Update" to save the updated information and to return to the main page, "Cancel" to cancel changes and to return to the main page, and "Delete" for deleting information about this place saved by the user.
9. A text field (optional) for comments about the place.

#### Adding a new place
(accessible by clicking "Add place" in menu\
only if the user is logged in, otherwise the user is redirected to Log in page)
1. A text field (required) for the place name.
2. A slider for setting the user's own opinion ("my opinion") about the place (by default 0).
3. A text field (required) for the country name.
4. A switch to indicate whether the place is visited (by default "No"). The user may add information about the place even before visiting it. This *a priori* opinion will be used for calculation of "Users' opinion" but not for calculation of "REC-opinion".
5. A text field (optional) for a link to a website about the place.
6. A text field (optional) for a link to a place image.
7. A text field (optional) for comments about the place.
8. Buttons "Add new place" to save the new information and to return to Home page, "Cancel" to cancel and to return to Home page.

#### Selecting countries
(accessible by clicking "Select" in menu)
1. The page title "Select".
2. A list of countries that can be selected (one, several, or all).
3. Buttons "Find places" to save the selection and to get to the Selected places page, "Cancel" to cancel and to return to the main page.

#### Selected places
(accessible by clicking "Find places" on Selecting countries page, see above)
This page is identical to Home page in all aspects except for 2 differences.
1. The page title is "Selected places".
2. Cards are displayed only for those places which countries were selected on Selecting countries page.

#### Recommended places
(accessible by clicking "RECommended" in menu\
only if the user is logged in, otherwise the user is redirected to Log in page)
This page is identical to Home page in all aspects except for 3 differences.
1. The page title is "RECommended places".
2. Cards are displayed only for those places for which REC-opinion can be calculated: (i) the place must not be visited by the user yet, (ii) the place must be visited by at least one user, (iii) there must be at least one place visited both by the logged in user and by at least one abovementioned user. Thus the user gets recommendations about **not yet visited** places which are **visited by other** users whose **tastes can be compared** to hers/his.
3. Instead of generic "Users' opinion", the "REC-opinion" calculated personally for the logged in user is shown on cards. The "REC-opinion" is also shown on Place details page if it was accessed from Recommended places page.

#### Login
(accessible by clicking "Login" in menu\
or redirected from Editing of place details, Adding a new place, or Recommended places pages if the user tried to access them without logging in\
or redirected from Login page in case of problems with logging in)
1. The page title is "Login".
2. A warning message (only in case of problems with logging in).
3. A text field (required) for the username.
4. A text field (required) for the password.
5. Buttons "Login" login and to return to Home page, "Cancel" to cancel and to return to Home page.
6. Buttons "Sign Up" to get to Signup page.

#### Singup
(accessible by clicking "Sign Up" on Login page\
or redirected from Signup page in case of problems with signing in)
1. The page title is "Sign Up".
2. A warning message (only in case of problems with signing up).
3. A text field (required) for the username.
4. A text field (required) for the password.
5. Buttons "Sign Up" to sign up and to return to Login page, "Cancel" to cancel and to return to Login page.

#### Help
(accessible by clicking "Help" in menu)
1. basic concepts of the site,
2. instructions for users,
3. contact address for complaints, suggestions, etc.


### Features Left to Implement:
**At the moment, a minimal usable version of the site is deployed. If there are many enough users interested in the site, many aspects can be imporved, for example:**
1. For each place several names can be used (e.g. names in different languages). When a user wants to add a new place the place's name is compared with place names in the database and one or several names (like Syracuse in Italy, Syracuse in NY, Syracuse in IN, etc.) of already saved places are prompted.
2. Each user can add unlimited number of photos, website links and comments.
3. For each place, its geographic coordinates and position on map can be added.
4. Each item (photo, website, comment) can be rated by users. And these ratings can be used for calculation of REC-opinion.
5. Parameters other than country name (e.g. parts of place name, range of Users' opinion, number of users who visited the place etc.) can be used for filtering place sets.
6. Standard sign up and log in (with email address) can be implemented so that a user can change her/his username, password, get new password to replace the forgotten one etc.

**Also the site's functionality can be expanded:**
1. A trip planner can be added. A user sets departure and arrival places, total number of trip days, minimal and maximal distances for a day trip, etc. Based on these data, the site recommends possible routes with places to visit and estimates of time to spend for the visits.
2. Other services (like sites of travel agencies, hotels or museums) can be added to such a planner.


## Technologies Used
The project was written with HTML5, CSS3, Javascript, Pyhton3, Flask, MongoDB.\
[Bootstrap] toolkit (https://getbootstrap.com/) was used for simple and clear design.


## Testing
The site was tested manually according to User stories (see UX section above).\
The site behaved as expected (as described in User stories) when entered information was valid. If the required information was missing (e.g. username and/or password on Signup page), a warning message appeared and the site waited for valid input.\
An attempt to sign up with an already used username resulted in a warning message and return to the sign up form. Similarly, an attempt to log in with erroneous username and/or password resulted in a warning message and return to the log in form.\
An attempt to use edit/add/recommended functionality without logging in resulted in redirect to Login page.

The site was designed to be used mainly on mobile phones with a small display.\
It was tested on a laptop Lenovo ThinkPad (with different window widths from 330px to 1466px) and a mobile phone Motorola XT1941 4.


## Deployment
The project is deployed to Heroku (built from the master branch):\
https://myRecs.herokuapp.com/ \
The source files are publicly accessible:\
https://github.com/pavzel/myRecs \
To run locally, you can clone this repository: paste `git clone https://github.com/pavzel/myRecs.git` into your terminal. To cut ties with this GitHub repository, type `git remote rm origin` into the terminal.
Private configuration variables (the link MONGO_URI that gives access to the MongoDB database, and the secret key SECRET used by Flask app) are not revealed.


## Credits
The photos saved in the database for this project are only from open sources like Wikipedia etc.\
The links saved in the database for this project are to open resources like Wikipedia, museum sites etc.\
The project idea was suggested by Code Institute.
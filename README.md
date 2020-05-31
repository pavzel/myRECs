### author: Pavel Zelenin
### Code Institute
### Full Stack Web Developer course
## Milestone Project #3
### (Practical Python and Data-Centric Development)
 
# Recommendation site myRecs

https://myRecs.herokuapp.com/


## Overview
The main purpose of this project (Milestone Project #3) was to build a full-stack site that allows users to manage a common dataset about a particular domain.
The site demonstrates some of my knowledge and skills in Python, Flask, MongoDB, and Heroku at the beginning of June 2020.

This site is for me and any other person who likes traveling by car. A car provides flexibility in terms of where and when to go, to stay for a night, what to visit, and how much time to spend for a visit. Travel results in memories that can be stored and shared together with personal opinions and recommendations. Thus a user can refresh own memories and get recommendations about new places to visit from other users.

All recommendations are place-centered. A place can have just one interesting site (like Mont-Saint-Michel) or hundreds of them (like Paris) but if these sites can be reached on foot or by car within 5-20 minutes, all of them are considered to be located in the same place.

For each place the following information is saved: name, country, personal opinion ("rating", details see below), a marker (visited or not visited), a link to a photo (optional), a link to a website (optional).

A place is rated by a user according to a scale:
    -3 means "never go there"
    -2 means "uninteresting and unfriendly"
    -1 means "boring"
     0 means "rather nice but nothing special"
    +1 means "interesting or especially nice"
    +2 means "very interesting"
    +3 means "outstanding/unique"
A user can see either own opinion, or summary opinion based on opinions of all users, or statistics of all opinions. Potentially, a custom "recommendation" based on similarity of tastes of a user with the other users, can be calculated.


## UX
(TO BE ADDED)

## Features
### Existing Features
(TO BE ADDED)

### Features Left to Implement:
(TO BE ADDED)
1. 
2.
3.


## Technologies Used
The project was written with HTML5, CSS3, Javascript, Pyhton3, Flask, MongoDB.\
[Materialize] framework (https://materializecss.com/) was used for simple and clear design. Another purpose was educational: to practice using the framework.


## Testing
The site was designed to be used mainly on mobile phones with a small display.\
It was tested on a laptop Lenovo ThinkPad (with different window widths from 330px to 1466px) and a mobile phone Motorola XT1941 4.



## Deployment
The project is deployed to Heroku (built from the master branch):\
https://myRecs.herokuapp.com/ \
The source files are publicly accessible:\
https://github.com/pavzel/myRecs\
To run locally, you can clone this repository: paste `git clone https://github.com/pavzel/myRecs.git` into your terminal. To cut ties with this GitHub repository, type `git remote rm origin` into the terminal.


## Credits
The project idea was suggested by Code Institute.\
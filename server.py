import json
from flask import Flask, render_template, request, redirect, flash, url_for

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions
    
def init_club_bookings(list_of_clubs, list_of_competitions):
    dict_bookings = {}
    for club in list_of_clubs:
        dict_bookings[club["name"]] = {}
        for competition in list_of_competitions:
            dict_bookings[club["name"]][competition["name"]] = 0

    return dict_bookings

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
bookings = init_club_bookings(clubs, competitions)

@app.route('/')
def index():
    return render_template('index.html'), 200

@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions), 200
    except IndexError:
        if request.form['email'] == " ":
            return render_template('index.html'), 401
        else:
            status_code = 401
            return render_template('index.html', error_message="Please enter a valid email"), status_code

@app.route('/book/<competition>/<club>')
def book(competition,club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition), 200
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions), 400
    except IndexError:
        flash("Something went wrong-please try again")
    return render_template('welcome.html', club=club, competitions=competitions), 404

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        placesCompetition = int(competition["numberOfPlaces"])
        clubPoints = int(club["points"])
        if placesRequired <= 0:
            flash("Cannot be less than or equal to 0")
        elif placesRequired > 12:
            flash("You may not reserve more than 12 places at a time.")
        elif placesRequired > placesCompetition:
            flash("Please note that you have selected more than the maximum number of places.")
        elif clubPoints < placesRequired:
            flash("You don't have enough points")
        else:
            competition['numberOfPlaces'] = placesCompetition - placesRequired
            club['points'] = clubPoints - placesRequired
            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions), 200
    except ValueError:
        flash('Please enter a number between 0 and 12.')
    return render_template('booking.html', club=club, competition=competition), 403

def get_competition_club(competition_name, club_name):
    competition = [c for c in competitions if c['name'] == competition_name][0]
    club = [c for c in clubs if c['name'] == club_name][0]
    return competition, club

def get_bookings(club_name, competition_name):
    return bookings[club_name][competition_name]

@app.route('/clubs')
def view_club_points():
    club_list = sorted(clubs, key=lambda club: club['name'])
    return render_template('list_clubs.html', clubs=club_list)

@app.route('/logout')
def logout():
    return redirect(url_for('index')), 200
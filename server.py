import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for
from Python_Testing.conf_app import update_places, list_places_booked, sorted_competitions

def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def init_club_bookings(list_of_clubs, list_of_competitions):
    dict_bookings = {}
    for club in list_of_clubs:
        dict_bookings[club["name"]] = {}
        for competition in list_of_competitions:
            dict_bookings[club["name"]][competition["name"]] = 0

    return dict_bookings


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()
bookings = init_club_bookings(clubs, competitions)
places_booked = list_places_booked(competitions, clubs)
old_competitions, new_competitions = sorted_competitions(competitions)


@app.route('/')
def index():
    return render_template('index.html'), 200


@app.route('/show-summary', methods=['POST'])
def show_summary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions), 200
    except IndexError:
        if request.form['email'] == " ":
            return render_template('index.html'), 401
        else:
            return render_template('index.html', error_message="Please enter a valid email"), 401


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        found_club = [c for c in clubs if c['name'] == club][0]
        found_competition = [c for c in competitions if c['name'] == competition][0]
        if datetime.strptime(found_competition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
            flash("this competition is over.")
        else:
            return render_template('booking.html', club=found_club, competition=found_competition), 200
    except IndexError:
        flash("Something went wrong-please try again")
    return render_template('welcome.html', club=club, old_competitions=old_competitions, new_competitions=new_competitions), 404


@app.route('/purchase-places', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    places_competition = int(competition["numberOfPlaces"])
    club_points = int(club["points"])
    if places_required <= 0:
        flash("Cannot be less than or equal to 0")
        return render_template('welcome.html', club=club, competitions=competitions)
    elif places_required > 12:
        flash("You may not reserve more than 12 places at a time.")
        return render_template('welcome.html', club=club, competitions=competitions)
    elif places_required > places_competition:
        flash("Please note that you have selected more than the maximum number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)
    elif club_points < places_required:
        flash("You don't have enough points")
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        try:
            update_places(competition, club, places_booked, places_required)
            competition['numberOfPlaces'] = places_competition - places_required
            club['points'] = club_points - places_required
            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions), 200
        except ValueError:
            flash('You may not reserve more than 12 places at a time.')

    return render_template('welcome.html', club=club, competition=competition)

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
    return redirect(url_for('index')), 301
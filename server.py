from datetime import datetime
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


def is_competition_past(competition_date_str):
    try:
        comp_date = datetime.strptime(competition_date_str, '%Y-%m-%d %H:%M:%S')
        return comp_date < datetime.now()
    except (ValueError, TypeError):
        return False


app = Flask(__name__)
app.secret_key = 'something_special'
app.jinja_env.filters['is_past'] = is_competition_past

def reset_data():
    global competitions, clubs, bookings_tracker
    competitions = loadCompetitions()
    clubs = loadClubs()
    bookings_tracker = {}


competitions = loadCompetitions()
clubs = loadClubs()
bookings_tracker = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form.get('email', '').strip()
    matching_clubs = [club for club in clubs if club['email'] == email]
    if not matching_clubs:
        flash("Sorry, that email was not found.")
        return render_template('index.html'), 401
    club = matching_clubs[0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if foundClub and foundCompetition:
        club_obj = foundClub[0]
        comp_obj = foundCompetition[0]
        if is_competition_past(comp_obj['date']):
            flash("Cannot book places for past competitions.")
            return render_template('welcome.html', club=club_obj, competitions=competitions)
        return render_template('booking.html', club=club_obj, competition=comp_obj)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for('index'))


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    if is_competition_past(competition['date']):
        flash("Cannot book places for past competitions.")
        return render_template('welcome.html', club=club, competitions=competitions)
    placesRequired = int(request.form['places'])
    club_points = int(club['points'])
    competition_places = int(competition['numberOfPlaces'])
    already_booked = bookings_tracker.get((club['name'], competition['name']), 0)

    if placesRequired > 12 or (already_booked + placesRequired) > 12:
        flash("You cannot book more than 12 places per competition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired > competition_places:
        flash("Not enough places available in this competition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired > club_points:
        flash("You do not have enough points to book these places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = str(club_points - placesRequired)
    bookings_tracker[(club['name'], competition['name'])] = already_booked + placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
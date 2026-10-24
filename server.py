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
        flash("Désolé, cette adresse email est introuvable.")
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
            flash("Impossible de réserver des places pour les compétitions passées.")
            return render_template('welcome.html', club=club_obj, competitions=competitions)
        if int(comp_obj['numberOfPlaces']) <= 0:
            flash("Cette compétition est complète.")
            return render_template('welcome.html', club=club_obj, competitions=competitions)
        return render_template('booking.html', club=club_obj, competition=comp_obj)
    else:
        flash("Une erreur est survenue, veuillez réessayer.")
        return redirect(url_for('index'))


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    if is_competition_past(competition['date']):
        flash("Impossible de réserver des places pour les compétitions passées.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if int(competition['numberOfPlaces']) <= 0:
        flash("Cette compétition est complète.")
        return render_template('welcome.html', club=club, competitions=competitions)

    try:
        placesRequired = int(request.form.get('places', 0))
        if placesRequired <= 0:
            flash("Veuillez saisir un nombre de places positif.")
            return render_template('welcome.html', club=club, competitions=competitions)
    except (ValueError, TypeError):
        flash("Nombre de places demandé invalide.")
        return render_template('welcome.html', club=club, competitions=competitions)

    club_points = int(club['points'])
    competition_places = int(competition['numberOfPlaces'])
    already_booked = bookings_tracker.get((club['name'], competition['name']), 0)

    if placesRequired > 12 or (already_booked + placesRequired) > 12:
        flash("Vous ne pouvez pas réserver plus de 12 places par compétition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired > competition_places:
        flash("Il n'y a pas assez de places disponibles dans cette compétition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired > club_points:
        flash("Vous n'avez pas assez de points pour réserver ces places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = str(club_points - placesRequired)
    bookings_tracker[(club['name'], competition['name'])] = already_booked + placesRequired
    flash('Super, réservation effectuée avec succès !')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/points')
def points():
    return render_template('points.html', clubs=clubs)


@app.route('/clubs')
def show_clubs():
    return redirect(url_for('points'))


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
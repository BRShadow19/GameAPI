import json
import riot
import tft
from flask import Flask, jsonify

app = Flask(__name__)

# TODO: Create methods and API routes for each of the game stats we want to obtain

@app.route('/league/mastery/<summoner>/<tagline>/<count>')
@app.route('/league/mastery/<summoner>/<tagline>')
def league_mastery(summoner, tagline, count="5"):
    print(count)
    champions = riot.get_top_champs(summoner, tagline, count)
    return jsonify(champions)


@app.route('/league/rank/<summoner>/<tagline>/<league>')
def league_rank(summoner, tagline, league="SOLO"):
    rank = riot.get_summoner_rank(summoner, tagline, league)
    return jsonify(rank)


@app.route('/league/matches/<summoner>/<tagline>/<count>')
@app.route('/league/matches/<summoner>/<tagline>')
def league_matches(summoner, tagline,  count="5"):
    matches = riot.get_matches(summoner, tagline, count)
    return jsonify(matches)

@app.route('/league/match/<summoner>/<tagline>/<start>')
@app.route('/league/match/<summoner>/<tagline>')
def league_one_match(summoner, tagline, start="1"):
    match = riot.get_matches(summoner, tagline, count="1", start=start)
    return jsonify(match)

@app.route('/tft/rank/<summoner>/<tagline>/<league>')
def tft_rank(summoner, tagline, league='RANKED'):
    rank = tft.get_tft_rank(summoner, tagline, league)
    return jsonify(rank)

@app.route('/tft/match/<summoner>/<tagline>/<start>')
@app.route('/tft/match/<summoner>/<tagline>')
def tft_match(summoner, tagline, start="1"):
    match = tft.get_match(summoner, tagline, count="1", start=start)
    return jsonify(match)

@app.route('/tft/matches/<summoner>/<tagline>/<count>')
@app.route('/tft/matches/<summoner>/<tagline>')
def tft_matches(summoner, tagline, count="10"):
    matches = tft.get_recents(summoner, tagline, count)
    return jsonify(matches)

# Define API route to handle unknown requests
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({'error': 'Invalid request'})

# Run Flask app
if __name__ == '__main__':
    app.run()
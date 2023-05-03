import json
import socket
import riot
import bungie
from flask import Flask, jsonify

app = Flask(__name__)

# TODO: Create methods and API routes for each of the game stats we want to obtain

@app.route('/league/mastery/<summoner>/<count>')
@app.route('/league/mastery/<summoner>')
def league_mastery(summoner, count="5"):
    print(count)
    champions = riot.get_top_champs(summoner, count)
    return jsonify(champions)


@app.route('/league/rank/<summoner>')
def league_rank(summoner):
    rank = riot.get_summoner_rank(summoner)
    return jsonify(rank)


@app.route('/league/matches/<summoner>/<count>')
@app.route('/league/matches/<summoner>')
def league_matches(summoner, count="5"):
    matches = riot.get_matches(summoner, count)
    return jsonify(matches)

# Define API route to handle unknown requests
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({'error': 'Invalid request'})

# Run Flask app
if __name__ == '__main__':
    app.run()
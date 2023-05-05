import json
import riot
from flask import Flask, jsonify

app = Flask(__name__)

# TODO: Create methods and API routes for each of the game stats we want to obtain

@app.route('/league/mastery/<summoner>/<count>')
@app.route('/league/mastery/<summoner>')
def league_mastery(summoner, count="5"):
    print(count)
    champions = riot.get_top_champs(summoner, count)
    return jsonify(champions)


@app.route('/league/rank/<summoner>/<league>')
def league_rank(summoner, league="SOLO"):
    rank = riot.get_summoner_rank(summoner, league)
    return jsonify(rank)


@app.route('/league/matches/<summoner>/<count>')
@app.route('/league/matches/<summoner>')
def league_matches(summoner, count="5"):
    matches = riot.get_matches(summoner, count)
    return jsonify(matches)

@app.route('/league/match/<summoner>/<start>')
@app.route('/league/match/<summoner>')
def league_one_match(summoner, start="1"):
    match = riot.get_matches(summoner, count="1", start=start)
    return jsonify(match)


# Define API route to handle unknown requests
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({'error': 'Invalid request'})

# Run Flask app
if __name__ == '__main__':
    app.run()
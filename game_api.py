import json
import socket
import riot
import bungie
from flask import Flask, jsonify

app = Flask(__name__)

# TODO: Create methods and API routes for each of the game stats we want to obtain




# Define API route to handle unknown requests
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({'error': 'Invalid request'})

# Run Flask app
if __name__ == '__main__':
    app.run()
"""
This file is for methods used in obtaining data from the Riot Games API. 
Here we will unpack the JSON response from Riot, pull out the specific info we want, and repackage it into
another JSON to be used in game_api.py
"""
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv('keys.env')    # Load environment variables from keys.env

TARGET = "https://na1.api.riotgames.com"
API_KEY = os.environ.get('RIOT_KEY')     # The Riot API bot token
CHAMPION_IDS = json.load(open("champion_ids", "r"))


# https://developer.riotgames.com/apis

# TODO: download data dragon, loop through the champions, and make a new JSON with the key:value pairs being championID:championName


# Example call
# https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Doublelift?api_key=RGAPI-YOUR-API-KEY

# TODO: Make methods that obtain the following data from the Riot API and pull out the info we want

# Top 5 champion masteries
def get_top_5_champs(summonerName):
    summonerID = get_summoner_id(summonerName)
    url = "https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"+summonerID+"/top?count=5&api_key="+API_KEY
    response = requests.get(url)
    data = response.json()
    for champion in data:
        pass

# Overview of last 5 games

# Detailed view of previous game

# Get the name of a champion by champion ID
def get_champion_name(championID):
    return CHAMPION_IDS[championID]

# Summoner rank
def get_summoner_rank(summonerName):
    encryptedID = get_summoner_id(summonerName)
    url = TARGET+"/lol/league/v4/entries/by-summoner/"+encryptedID+"?api_key="+API_KEY
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return (data["tier"], data["rank"])
    else: 
        return -1


# Encrypted summoner ID
def get_summoner_id(summonerName):
    url = TARGET+"/lol/summoner/v4/summoners/by-name/"+summonerName+"?api_key="+API_KEY
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data["id"]
    else: 
        return -1


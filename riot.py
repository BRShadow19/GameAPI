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
def get_top_5_champs(summoner_name):
    ret = {}
    summoner_id = get_summoner_id(summoner_name)
    if len(summoner_id) > 0:    # Make sure we get a valid summoner ID
        url = TARGET+"/lol/champion-mastery/v4/champion-masteries/by-summoner/"+summoner_id+"/top?count=5&api_key="+API_KEY
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() # List of match IDs
            matches = {}
            for match_id in data:
                pass
            ret = matches
    return ret
    
# Get detailed stats on the last match
def get_match_info(match_id):
    ret = {}
    url = TARGET+"lol/match/v5/matches/"+match_id+"?api_key="+API_KEY
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        

# Overview of last 5 games
def get_last_five_games(summoner_name):
    ret = {}
    puuid = get_summoner_puuid(summoner_name)
    if len(puuid) > 0:    # Make sure we get a valid summoner ID
        url = TARGET+"/lol/match/v5/matches/by-puuid/"+puuid+"/ids?api_key="+API_KEY
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() # List of dictionaries
            champion_data = {}
            for champion in data:
                champion_id = champion["championId"]
                champion_name = get_champion_name(champion_id)
                mastery_level = champion["championLevel"]
                mastery_points = champion["championPoints"]
                champion_data[champion_name] = (mastery_level, mastery_points)
            ret = champion_data
    return ret

# Detailed view of previous game

# Get the name of a champion by champion ID
def get_champion_name(champion_id):
    return CHAMPION_IDS[champion_id]

# Summoner rank
def get_summoner_rank(summoner_name):
    ret = []
    encryptedID = get_summoner_id(summoner_name)
    if encryptedID != -1:
        url = TARGET+"/lol/league/v4/entries/by-summoner/"+encryptedID+"?api_key="+API_KEY
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            ret = [data["tier"], data["rank"]]
    return ret
    


# Encrypted summoner ID
def get_summoner_id(summoner_name):
    """Call the Riot API to get the encrypted summoner ID corresponding to a given summoner name

    Args:
        summoner_name (str): The name of the summoner whose ID we want

    Returns:
        str: The encrypted summoner ID. Will return an empty string if we get an invalid response from Riot
    """
    ret = ""
    url = TARGET+"/lol/summoner/v4/summoners/by-name/"+summoner_name+"?api_key="+API_KEY
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        ret = data["id"]
    return ret

# Summoner PUUID
def get_summoner_puuid(summoner_name):
    """Call the Riot API to get the unique internal player ID corresponding to a given summoner name

    Args:
        summoner_name (str): The name of the summoner whose puuid we want

    Returns:
        str: The unique summoner puuid. Will return an empty string if we get an invalid response from Riot
    """
    ret = ""
    url = TARGET+"/lol/summoner/v4/summoners/by-name/"+summoner_name+"?api_key="+API_KEY
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        ret = data["puuid"]
    return ret

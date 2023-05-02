"""
This file is for methods used in obtaining data from the Riot Games API. 
Here we will unpack the JSON response from Riot, pull out the specific info we want, and repackage it into
another JSON to be used in game_api.py
"""
import json
import requests
import os
import datetime
from dotenv import load_dotenv
load_dotenv('keys.env')    # Load environment variables from keys.env

TARGET = "https://na1.api.riotgames.com"
API_KEY = os.environ.get('RIOT_KEY')     # The Riot API bot token
CHAMPION_IDS = json.load(open("champion_ids.json", "r"))


# https://developer.riotgames.com/apis

# Example call
# https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Doublelift?api_key=RGAPI-YOUR-API-KEY


def get_top_5_champs(summoner_name):
    """Call the Riot API to obtain the top 5 champions of a summoner based on mastery points

    Args:
        summoner_name (str): The name of the summoner whose list of champions we want

    Returns:
        dict {str: tuple of ints} -> {"champion_name" : (mastery_level, mastery_points)}
            A dictionary where the key is the champion's name, and the value is a tuple containing the 
                mastery level and mastery points for that champion. Returns an empty dictionary if an
                invalid response is received from the API
    """
    ret = {}
    summoner_id = get_summoner_id(summoner_name)
    if len(summoner_id) > 0:    # Make sure we get a valid summoner ID
        url = TARGET+"/lol/champion-mastery/v4/champion-masteries/by-summoner/"+summoner_id+"/top?count=5&api_key="+API_KEY
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() # List of dictionaries
            champion_data = {}
            for champion in data:
                champion_id = str(champion["championId"])   # Stored as an int in the JSON response, need to cast it to a string
                champion_name = get_champion_name(champion_id)
                mastery_level = champion["championLevel"]
                mastery_points = champion["championPoints"]
                champion_data[champion_name] = (mastery_level, mastery_points)
            ret = champion_data
    return ret
    

def get_match_info(match_id, puuid):
    """Calls the Riot API to get detailed stats on specific match in relationship to a summoner based on the match ID. 
    Stats obtained are: win/loss (boolean), KDA (string, kills/deaths/assists), total CS (int), CS/min (float), 
    game duration (string, hours:minutes:seconds), damage to champions (int), and champion name (string.)

    Args:
        match_id (str): Unique ID of the requested match
        puuid (str): Unique player ID of the requested summoner

    Returns:
        dict: Dictionary containing stats about the game. Returns an empty dictionary if an invalid response is received from the API.
            Example: {  'win': True, 
                        'KDA': '2/8/14', 
                        'CS': 57, 
                        'CS/min': 1.5, 
                        'duration': '0:38:59', 
                        'championDamage': 19409, 
                        'championName': 'Lux'
                     }
    """
    ret = {}
    # Different API target than some other methods, so not using the TARGET variable
    url = "https://americas.api.riotgames.com/lol/match/v5/matches/"+match_id+"?api_key="+API_KEY
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # participant index = metadata->participants->list.index(puuid)
        participant_idx = data["metadata"]["participants"].index(puuid)
        # win/loss = info->participants[index]->win
        win = data["info"]["participants"][participant_idx]["win"]
        # number of kills = info->participants[index]->kills
        num_kills = str(data["info"]["participants"][participant_idx]["kills"])
        # number of deaths = info->participants[index]->deaths
        num_deaths = str(data["info"]["participants"][participant_idx]["deaths"])
        # number of assists = info->participants[index]->assists
        num_assists = str(data["info"]["participants"][participant_idx]["assists"])
        
        champion_name = data["info"]["participants"][participant_idx]["championName"] 
        # CS (creep score) = info->participants[index]->totalMinionsKilled
        cs = data["info"]["participants"][participant_idx]["totalMinionsKilled"]    # Lane minions
        cs += data["info"]["participants"][participant_idx]["neutralMinionsKilled"]    # Jungle minions
        # game duration in seconds = info->gameDuration
            # Convert to minutes: str(datetime.timedelta(seconds=gameDuration))
            # hours:minutes:seconds
            # or for CS/min, just do minutes=gameDuration/60
        duration_seconds = data["info"]["gameDuration"]
        duration_time = str(datetime.timedelta(seconds=duration_seconds))
        duration_minutes = duration_seconds/60
        cs_per_minute = round(cs/duration_minutes, 1) # round to one decimal place
        # damage to champions = info->participants[index]->totalDamageDealtToChampions
        champion_damage = data["info"]["participants"][participant_idx]["totalDamageDealtToChampions"]
        ret = {
            "win": win,
            "KDA": num_kills+"/"+num_deaths+"/"+num_assists,
            "CS": cs,
            "CS/min": cs_per_minute,
            "duration": duration_time,
            "championDamage": champion_damage,
            "championName": champion_name
        }
        
    return ret
        

def get_last_five_games(summoner_name):
    """Call the Riot API to obtain stats about the 5 most recent games of a given summoner. 

    Args:
        summoner_name (str): The name of the summoner whose ranked information we want

    Returns:
        list: List of dictionaries, with each one containing information about a match. Returns an empty list 
                if an invalid response is received from the API.
                Example dictionary: {   'win': True, 
                                        'KDA': '2/8/14', 
                                        'CS': 57, 
                                        'CS/min': 1.5, 
                                        'duration': '0:38:59', 
                                        'championDamage': 19409, 
                                        'championName': 'Lux'
                                    }
    """
    ret = []
    puuid = get_summoner_puuid(summoner_name)
    if len(puuid) > 0:    # Make sure we get a valid summoner ID
        # Different API target than some other methods, so not using the TARGET variable
        url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count=5&api_key="+API_KEY
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() # List of match IDs
            for match_id in data:
                match = get_match_info(match_id, puuid)
                ret.append(match)           
            
    return ret


def get_champion_name(champion_id):
    """Convert a champion ID into the corresponding champion name

    Args:
        champion_id (str): The ID of the champion whose name we want

    Returns:
        str: The name of the champion
    """
    return CHAMPION_IDS[champion_id]


def get_summoner_rank(summoner_name):
    """Call the Riot API to get a summoner's ranked tier, division, and number of LP (i.e, SILVER II 42LP)

    Args:
        summoner_name (str): The name of the summoner whose ranked information we want

    Returns:
        list: Contains the tier, division, and LP of the player at indices 0, 1, and 2, respectively. Returns an empty list if
                an invalid response is received from the API.
    """
    ret = []
    encryptedID = get_summoner_id(summoner_name)
    if len(encryptedID) > 0 :
        url = TARGET+"/lol/league/v4/entries/by-summoner/"+encryptedID+"?api_key="+API_KEY
        response = requests.get(url)
        data = response.json()[0]
        if response.status_code == 200:
            ret = [data["tier"], data["rank"], data["leaguePoints"]]
    return ret
    

def get_summoner_id(summoner_name):
    """Call the Riot API to get the encrypted summoner ID corresponding to a given summoner name

    Args:
        summoner_name (str): The name of the summoner whose ID we want

    Returns:
        str: The encrypted summoner ID. Returns an empty string if an invalid response is received from the API.
    """
    ret = ""
    url = TARGET+"/lol/summoner/v4/summoners/by-name/"+summoner_name+"?api_key="+API_KEY
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        ret = data["id"]
    return ret


def get_summoner_puuid(summoner_name):
    """Call the Riot API to get the unique internal player ID corresponding to a given summoner name

    Args:
        summoner_name (str): The name of the summoner whose puuid we want

    Returns:
        str: The unique summoner puuid. Returns an empty string if an invalid response is received from the API.
    """
    ret = ""
    url = TARGET+"/lol/summoner/v4/summoners/by-name/"+summoner_name+"?api_key="+API_KEY
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        ret = data["puuid"]
    return ret

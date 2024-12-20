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
ACCOUNT_TARGET = "https://americas.api.riotgames.com"
API_KEY = os.environ.get('RIOT_KEY')     # The Riot API bot token
# TFT_KEY = os.environ.get('TFT_KEY')   # To be used later for TFT
CHAMPION_IDS = json.load(open(os.path.join('./data-jsons', "champion_ids.json"), "r"))
# Adapted from https://static.developer.riotgames.com/docs/lol/queues.json
GAME_IDS = json.load(open(os.path.join('./data-jsons', "queue_ids.json"), "r"))
# https://developer.riotgames.com/apis

# Example call
# https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Doublelift?api_key=RGAPI-YOUR-API-KEY


def get_top_champs(summoner_name, tagline, count):
    """Call the Riot API to obtain the top <count> champions of a summoner based on mastery points

    Args:
        summoner_name (str): The name of the summoner whose list of champions we want
        count (str): The number of champions to obtain       
    Returns:
        dict {str: list of ints} -> {"champion_name" : [mastery_level, mastery_points]}
            A dictionary where the key is the champion's name, and the value is a list containing the 
                mastery level and mastery points for that champion. Returns an empty dictionary if an
                invalid response is received from the API
    """
    ret = {}
    print("start of get_top_champs")
    #print(str(summoner_name) + str(tagline))
    puuid = get_summoner_puuid(summoner_name, tagline)
    print(str(len(puuid)))
    #summoner_id = get_summoner_id(summoner_name)
    if len(puuid) > 0:    # Make sure we get a valid summoner ID
        #url = TARGET+"/lol/champion-mastery/v4/champion-masteries/by-summoner/"+summoner_id+"/top?count="+count+"&api_key="+API_KEY
        #puuid = get_summoner_puuid(summoner_name)
        url = TARGET+"/lol/champion-mastery/v4/champion-masteries/by-puuid/"+puuid+"/top?count="+count+"&api_key="+API_KEY
        response = requests.get(url)
        print(url)
        print("code: " + str(response.status_code))
        if response.status_code == 200:
            print("YAY!")
            data = response.json() # List of dictionaries
            print(data)
            champion_data = {}
            for champion in data:
                champion_id = str(champion["championId"])   # Stored as an int in the JSON response, need to cast it to a string
                champion_name = get_champion_name(champion_id)
                mastery_level = champion["championLevel"]
                mastery_points = champion["championPoints"]
                champion_data[champion_name] = [mastery_level, mastery_points]
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
                        'CS': '57', 
                        'CS/min': '1.5', 
                        'duration': '0:38:59', 
                        'championDamage': '19409', 
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
        
        # Pull out all the data that we need
        champion_name = data["info"]["participants"][participant_idx]["championName"] 
        cs = data["info"]["participants"][participant_idx]["totalMinionsKilled"]    # Lane minions
        cs += data["info"]["participants"][participant_idx]["neutralMinionsKilled"]    # Jungle minions
        duration_seconds = data["info"]["gameDuration"] # Game duration in seconds
        duration_time = str(datetime.timedelta(seconds=duration_seconds))   # Duration in time format (HH:MM:SS)
        duration_minutes = duration_seconds/60  # Duration in minutes, used for calculating <stat> per minute
        cs_per_minute = round(cs/duration_minutes, 1) # round to one decimal place
        champion_damage = data["info"]["participants"][participant_idx]["totalDamageDealtToChampions"]  # Total damage dealt to enemy champions
        damage_per_minute = round(champion_damage/duration_minutes, 1)  # round to one decimal place
        vision_score = data["info"]["participants"][participant_idx]["visionScore"] 
        self_mitigated_damage = data["info"]["participants"][participant_idx]["damageSelfMitigated"]    # Total incoming damage that was self-mitigated (armor, magic resist, damage reduction)
        gold_earned = data["info"]["participants"][participant_idx]["goldEarned"]   # Total gold earned during the match
        gold_per_minute = round(gold_earned/duration_minutes, 1)    # round to one decimal place
        queue_id = str(data["info"]["queueId"]) # The internal ID number of the queue type (draft, blind, solo ranked, ARAM, etc)
        queue_name = GAME_IDS[0][queue_id]  # Actual name of the queue type
        multikill = data["info"]["participants"][participant_idx]["largestMultiKill"]   # Number of the largest multikill the player had
        multikill_type = "Single Kill"  # Default to "Single Kill," but change if they got something higher (each one is less likely than the previous)
        if multikill == 2:
            multikill_type = "Double Kill"
        elif multikill == 3:
            multikill_type = "Triple Kill!"
        elif multikill == 4:
            multikill_type = "Quadra Kill!!"
        elif multikill == 5:
            multikill_type = "PENTA KILL!!!"
        # Throw all of our data into a dictionary, and convert most of the numbers to strings
        ret = {
            "win": win,
            "KDA": num_kills+"/"+num_deaths+"/"+num_assists,
            "CS": str(cs),
            "CS/min": str(cs_per_minute),
            "duration": duration_time,
            "championDamage": str(champion_damage),
            "championName": champion_name,
            "visionScore": str(vision_score),
            "selfMitigatedDamage": str(self_mitigated_damage),
            "goldEarned": str(gold_earned),
            "largestMultikill": multikill,
            "multikillType": multikill_type,
            "queueType": queue_name,
            "gold/min": str(gold_per_minute),
            "damage/min": str(damage_per_minute)
        }
        
    return ret
        

def get_matches(summoner_name, tagline, count, start="1"):
    """Call the Riot API to obtain stats about the <count> most recent matches of a given summoner, starting at 
        a given amount of matches backwards. 

    Args:
        summoner_name (str): The name of the summoner whose match history we want
        count (str): The number of games we want to get info about
        start (str): The number of the match to start looking back from (1 would be the most recent game, 2 would be two games ago, etc).
                        Defaults to "1"

    Returns:
        list: List of dictionaries, with each one containing information about a match. Returns an empty list 
                if an invalid response is received from the API.
                Example dictionary: {
                                        "CS": "64",
                                        "CS/min": "2.0",
                                        "KDA": "3/0/18",
                                        "championDamage": "9991",
                                        "championName": "Thresh",
                                        "damage/min": "313.7",
                                        "duration": "0:31:51",
                                        "gold/min": "310.6",
                                        "goldEarned": "9892",
                                        "largestMultikill": 1,
                                        "multikillType": "Single Kill",
                                        "queueType": "Draft Pick",
                                        "selfMitigatedDamage": "17306",
                                        "visionScore": "83",
                                        "win": true
                                    }
    """
    ret = []
    puuid = get_summoner_puuid(summoner_name, tagline)
    if len(puuid) > 0:    # Make sure we get a valid summoner ID
        # Different API target than some other methods, so not using the TARGET variable
        start_int = int(start)
        # Riot API zero-indexes games, so subtract one
        if start_int > 0:
            start_int -= 1
        start = str(start_int)
        # Different API target than some other methods, so not using the TARGET variable
        url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start="+start+"&count="+count+"&api_key="+API_KEY
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

league_codes =  {   "SOLO": "RANKED_SOLO_5x5",
                    "FLEX": "RANKED_FLEX_SR"
                }

def get_summoner_rank(summoner_name, tagline, league_type="SOLO"):
    """Call the Riot API to get a summoner's ranked tier, division, and number of LP (i.e, SILVER II 42LP) 
        within a specific league type (solo or flex)

    Args:
        summoner_name (str): The name of the summoner whose ranked information we want
        league_type (str): The name of the league we want (SOLO or FLEX)

    Returns:
        list: Contains the tier, division, and LP of the player at indices 0, 1, and 2, respectively. Returns an empty list if
                an invalid response is received from the API.
    """
    ret = []
    puuid = get_summoner_puuid(summoner_name, tagline)
    encryptedID = get_summoner_id(puuid)
    if len(encryptedID) > 0 :
        url = TARGET+"/lol/league/v4/entries/by-summoner/"+encryptedID+"?api_key="+API_KEY
        response = requests.get(url)
        if response.status_code == 200:
            if league_type in league_codes:
                code = league_codes[league_type]
            else:
                code = league_codes["SOLO"]
            data = response.json()
            for league in data:
                if league["queueType"] == code:
                    ret = [league["tier"], league["rank"], league["leaguePoints"]]
    return ret
    

def get_summoner_id(puuid):
    """Call the Riot API to get the encrypted summoner ID corresponding to a given summoner name

    Args:
        summoner_name (str): The name of the summoner whose ID we want

    Returns:
        str: The encrypted summoner ID. Returns an empty string if an invalid response is received from the API.
    """
    ret = ""
    url = TARGET+"/lol/summoner/v4/summoners/by-puuid/"+ puuid + "?api_key="+API_KEY
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        ret = data["id"]
    return ret


def get_summoner_puuid(summoner_name, tagline):
    """Call the Riot API to get the unique internal player ID corresponding to a given summoner name

    Args:
        summoner_name (str): The name of the summoner whose puuid we want

    Returns:
        str: The unique summoner puuid. Returns an empty string if an invalid response is received from the API.
    """   
    ret = ""  
    url = ACCOUNT_TARGET+"/riot/account/v1/accounts/by-riot-id/"+ summoner_name + "/" + tagline + "?api_key="+API_KEY
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        ret = data["puuid"]
    return ret

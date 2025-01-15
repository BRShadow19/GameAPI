
import json
import requests
import os
import datetime
from dotenv import load_dotenv
load_dotenv('keys.env')

TARGET = "https://na1.api.riotgames.com"
ACCOUNT_TARGET = "https://americas.api.riotgames.com"
API_KEY = os.environ.get('TFT_KEY')

tft_codes = {
    "SOLO" : "RANKED_TFT",
    "DOUBLEUP" : "RANKED_TFT_DOUBLE_UP"
}

def get_tft_rank(summoner_name, tagline, league_type="RANKED"):
    """Call the Riot API to get a summoner's TFT ranked tier, division, and number of LP (i.e, SILVER II 42LP) 
        within a specific league type (normal ranked (RANKED) or double up (DOUBLEUP))

    Args:
        summoner_name (str): The name of the summoner whose ranked information we want
        league_type (str): The name of the league we want (RANKED or DOUBLEUP)

    Returns:
        list: Contains the tier, division, and LP of the player at indices 0, 1, and 2, respectively. Returns an empty list if
                an invalid response is received from the API.
    """
    ret = []
    puuid = get_summoner_puuid(summoner_name, tagline)
    encryptedID = get_summoner_id(puuid)
    if len(encryptedID) > 0 :
        url = TARGET+"/tft/league/v1/entries/by-summoner/"+encryptedID+"?api_key="+API_KEY
        response = requests.get(url)
        if response.status_code == 200:
            if league_type in tft_codes:
                code = tft_codes[league_type]
            else:
                code = tft_codes["SOLO"]
            data = response.json()
            for league in data:
                if league["queueType"] == code:
                    ret = [league["tier"], league["rank"], league["leaguePoints"]]
    return ret


def get_match_info(match_id, puuid):
    ret = {}
    url = "https://americas.api.riotgames.com/tft/match/v1/matches/"+match_id+"?api_key="+API_KEY
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        participant_idx = data["metadata"]["participants"].index(puuid)
        win = data["info"]["participants"][participant_idx]["win"]
        placement = str(data["info"]["participants"][participant_idx]["placement"])
        level = str(data["info"]["participants"][participant_idx]["level"])
        #turning the total round from the API response into the stage-round format used in game
        #                               ie: round 30 ---> stage 5 round 5, or round 5-5
        stage = ((data["info"]["participants"][participant_idx]["last_round"] - 4) // 7) + 2
        round = (data["info"]["participants"][participant_idx]["last_round"] -4 ) % 7
        round_reached = str(stage) + "-" + str(round)
        duration_seconds = data["info"]["participants"][participant_idx]["time_eliminated"]
        duration_time = str(datetime.timedelta(seconds=duration_seconds))   # Duration in time format (HH:MM:SS)
        traits = []
        for trait in data["info"]["participants"][participant_idx]["traits"]:
            
            to_add={
                "name" : trait["name"][6:], #removing "TFT13_" in the name
                #number of units of this trait that are active. used to sort when there are multiple traits of the same style 
                #                                                                                   ie: scrap 6 > ambusher 5
                "num_units" : trait["num_units"],
                #inactive=0, bronze=1, silver=2, unique=3, gold=4, pris=5. first level of sorting for later
                "style" : trait["style"]
            }
            
            traits.append(to_add)
        sorted_traits = sorted(traits, key=lambda x:x["style"], reverse=True)
        units = []
        for unit in data["info"]["participants"][participant_idx]["units"]:
            #because they are a little silly and index their costs really weirdly (1-3 cost are 0-2, 4 cost is 4, 5 is 6, 6 is 8)
            if unit["rarity"] < 4:
                cost = unit["rarity"] + 1
            if unit["rarity"] == 4:
                cost = unit["rarity"]
            if unit["rarity"] == 6:
                cost = unit["rarity"] - 1
            if unit["rarity"] == 8:
                cost = unit["rarity"] - 2
            
            to_add={
                "name" : unit["character_id"][6:], #removing "TFT_" in the name
                "cost" : str(cost),
                "star" : str(unit["tier"]),
                "sort_val" : (cost*0.6) + 2**(unit["tier"]/1.5)
            }
            units.append(to_add)
        sorted_units = sorted(units, key=lambda x:x["sort_val"], reverse=True)

        ret = {
            "placement" : placement,
            "win" : win,
            "level" : level,
            "round" : round_reached,
            "time_elim" : duration_time,
            "traits" : sorted_traits,
            "units" : sorted_units
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
        url = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/"+puuid+"/ids?start="+start+"&count="+count+"&api_key="+API_KEY
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() # List of match IDs
            for match_id in data:
                match = get_match_info(match_id, puuid)
                ret.append(match)           
            
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

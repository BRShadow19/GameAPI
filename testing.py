import json

file = open("champion.json", "r")
champions = json.load(file)

champion_ids = {}
data = champions["data"]
for championName in data:
    champion_ids[data[championName]["key"]] = championName

with open('champion_ids.json', 'w') as file:
    # Write dictionary as JSON string to file
    json.dump(champion_ids, file)
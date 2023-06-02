import requests
import json
import os
from dotenv import load_dotenv
import time


load_dotenv()
api_key = os.getenv("api_key") 
print(api_key)

puuid_api_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"
#summonerName = input("Enter your summoner name: ")

summonerName = "Phenomenalish"
puuid_api_url_filled = puuid_api_url.format(summonerName, api_key)
PUUID = requests.get(puuid_api_url_filled).json()["puuid"]


match_history_api_url = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?startTime=1673312400&queue=420&type=ranked&start={}&count=100&api_key={}"
matchlist = []

api_url_filled = match_history_api_url.format(PUUID, len(matchlist), api_key)

response = requests.get(api_url_filled)
responseJson = response.json()
responseCode = response.status_code
matchlist = matchlist + responseJson
while(len(responseJson) == 100):
    api_url_filled = match_history_api_url.format(PUUID, len(matchlist), api_key)
    response = requests.get(api_url_filled)
    responseJson = response.json()
    responseCode = response.status_code
    matchlist = matchlist + responseJson

print(len(matchlist))

match_api_url = "https://europe.api.riotgames.com/lol/match/v5/matches/{}?api_key={}"

data = []
kills = []
deaths = []
assists = []
outcomes = []
gameDuration = []
totalMinionsKilled = []


for match in matchlist:
    api_url_filled = match_api_url.format(match, api_key)
    try:
        response = requests.get(api_url_filled)
        responseJson = response.json()
        responseCode = response.status_code
        if responseCode == 200 and responseJson["info"]["gameDuration"] > 210:
            parts = responseJson["info"]["participants"]
            summNames = [d["summonerName"] for d in parts]
            index = summNames.index(summonerName)

            #data.append({"deaths": parts[index]["deaths"], "win": parts[index]["win"]})
            deaths.append(parts[index]["deaths"])
            kills.append(parts[index]["kills"])
            assists.append(parts[index]["assists"])
            outcomes.append(int(parts[index]["win"]))
            totalMinionsKilled.append(parts[index]["totalMinionsKilled"])
            gameDuration.append(responseJson["info"]["gameDuration"] / 60)
            print("Game {} out of {}".format(matchlist.index(match), len(matchlist)))
        else:
            if responseCode != 200:
                raise KeyError()
    except KeyError:
        time.sleep(120)

    
file = open("deaths.txt", "w")
file.write(str(deaths))
file.close()

file = open("outcomes.txt", "w")
file.write(str(outcomes))
file.close()

file = open("kills.txt", "w")
file.write(str(kills))
file.close()

file = open("assists.txt", "w")
file.write(str(assists))
file.close()

file = open("duration.txt", "w")
file.write(str(gameDuration))
file.close()

file = open("creeps.txt", "w")
file.write(str(totalMinionsKilled))
file.close()
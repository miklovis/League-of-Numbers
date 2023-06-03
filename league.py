import requests
import json
import os
from dotenv import load_dotenv
import time
import correlation


load_dotenv()
api_key = os.getenv("api_key") 

puuid_api_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"
summonerName = input("Enter your summoner name: ")

puuid_api_url_filled = puuid_api_url.format(summonerName, api_key)
PUUID = requests.get(puuid_api_url_filled).json()["puuid"]
folder_path = f"data/{PUUID}/"


match_history_api_url = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?startTime=1673312400&queue=420&type=ranked&start={}&count=100&api_key={}"
matchlist = []
api_url_filled = match_history_api_url.format(PUUID, len(matchlist), api_key)

data = {
    'outcome': [],
    'kills': [],
    'deaths': [], 
    'assists': [],
    'minions_killed': [],
    'vision_score': [],
    'position': [], #0 for top, 1 for jungle, 2 for mid, 3 for ADC, 4 for support
    'kill_participation': [],
    'game_duration': [],

    'net_kills': [],
    'net_deaths': [],
    'net_assists': [],
    'net_minions_killed': [],
    'net_vision_score': [],
    'net_kill_participation': []
}


cached_matchlist = []
'''
if os.path.exists(folder_path):
    with open(os.path.join(folder_path, f"{PUUID}_matchlist.json"), 'r') as file:
        cached_matchlist = json.load(file)

    with open(os.path.join(folder_path, f"{PUUID}_data.json"), 'r') as file:
        data = json.load(file)
'''
print(data)

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


matchlist = [x for x in matchlist if x not in cached_matchlist]

match_api_url = "https://europe.api.riotgames.com/lol/match/v5/matches/{}?api_key={}"

for match in matchlist:
    api_url_filled = match_api_url.format(match, api_key)
    try:
        response = requests.get(api_url_filled)
        responseJson = response.json()
        responseCode = response.status_code
        if responseCode == 200 and responseJson["info"]["gameDuration"] > 210:
            parts = responseJson["info"]["participants"]
            summNames = [d["summonerName"] for d in parts]
            roles = [d["individualPosition"] for d in parts]
            index = summNames.index(summonerName)
            enemyIndex = -1


            data['outcome'].append(int(parts[index]["win"]))
            data['deaths'].append(parts[index]["deaths"])
            data['kills'].append(parts[index]["kills"])
            data['assists'].append(parts[index]["assists"])
            data['minions_killed'].append(parts[index]["totalMinionsKilled"] + parts[index]["neutralMinionsKilled"])
            data['kill_participation'].append(round(parts[index]["challenges"]["killParticipation"], 2))
            data['vision_score'].append(parts[index]["visionScore"])
            match parts[index]["individualPosition"]:
                case "TOP":
                    data['position'].append(0)
                    for i, role in enumerate(roles):
                        if role == "TOP" and i != index:
                            enemyIndex = i
                            print(summNames[i] + " " + match)

                
                case "JUNGLE":
                    data['position'].append(1)
                    for i, role in enumerate(roles):
                        if role == "JUNGLE" and i != index:
                            enemyIndex = i
                            print(summNames[i] + " " + match)

                case "MIDDLE":
                    data['position'].append(2)
                    for i, role in enumerate(roles):
                        if role == "MIDDLE" and i != index:
                            enemyIndex = i
                            print(summNames[i] + " " + match)

                case "BOTTOM":
                    data['position'].append(3)
                    for i, role in enumerate(roles):
                        if role == "BOTTOM" and i != index:
                            enemyIndex = i
                            print(summNames[i] + " " + match)


                case "UTILITY":
                    data['position'].append(4)
                    for i, role in enumerate(roles):
                        if role == "UTILITY" and i != index:
                            enemyIndex = i
                            print(summNames[i] + " " + match)

                case _:
                    continue

            if enemyIndex == -1:
                enemyIndex = roles.index("Invalid")
                print(summNames[enemyIndex] + " " + match)

            data['net_kills'].append(parts[index]["kills"] - parts[enemyIndex]["kills"])
            data['net_deaths'].append(parts[index]["deaths"] - parts[enemyIndex]["deaths"])
            data['net_assists'].append(parts[index]["assists"] - parts[enemyIndex]["assists"])
            data['net_minions_killed'].append((parts[index]["totalMinionsKilled"] + parts[index]["neutralMinionsKilled"]) - (parts[enemyIndex]["totalMinionsKilled"] + parts[enemyIndex]["neutralMinionsKilled"]))
            data['net_vision_score'].append(parts[index]["visionScore"] - parts[enemyIndex]["visionScore"])
            data['net_kill_participation'].append(parts[index]["challenges"]["killParticipation"] - parts[enemyIndex]["challenges"]["killParticipation"])



            data['game_duration'].append(responseJson["info"]["gameDuration"] / 60)
            
            print("Game {} out of {}".format(matchlist.index(match) + 1, len(matchlist)))
        else:
            if responseCode != 200:
                raise KeyError()
    except KeyError:
        time.sleep(120)


os.makedirs(folder_path, exist_ok=True)
with open(f'data/{PUUID}/{PUUID}_matchlist.json', 'w') as file:
    json.dump(matchlist, file, ensure_ascii=True)
    
with open(f'data/{PUUID}/{PUUID}_data.json', 'w') as file:
    json.dump(data, file, ensure_ascii=True)

with open('data.json', 'w') as file:
    json.dump(data, file, ensure_ascii=True)



correlation.main()
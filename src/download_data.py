
# get the data for one game
# https://statsapi.web.nhl.com/api/v1/game/2022020001/boxscore

import requests
import json


game = requests.get('https://statsapi.web.nhl.com/api/v1/game/2022020001/boxscore')
print(game.status_code)
print(game.json())
print(type(game.json()))
json = game.json()
print(json.get("teams"))
away_team = json["teams"]["away"]
print(away_team)

# what do I want to know
# game date
# home and away teams
# team.name
# team.id
# winner - home or away






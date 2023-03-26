
# get the data for one game
# https://statsapi.web.nhl.com/api/v1/game/2022020001/boxscore

import requests
import json


def display_game(game):
    # home team data
    home_team = game["teams"]["home"]
    home_name = home_team["team"]["name"]
    home_score = home_team["score"]

    # away team data
    away_team = game["teams"]["away"]
    away_name = away_team["team"]["name"]
    away_score = away_team["score"]



    print("--------------------------------------------------")
    home_winner = home_score > away_score
    team_name_pad = 25
    home_winner_string = " <-- Winner" if home_winner else ""
    away_winner_string = " <-- Winner" if not home_winner else ""
    print("Away :  " + away_name.ljust(team_name_pad) + " : " + str(away_score) + away_winner_string)
    print("Home :  " + home_name.ljust(team_name_pad) + " : " + str(home_score) + home_winner_string)



start_date = "2023-03-01"
end_date = "2023-03-24"
url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + start_date + "&endDate=" + end_date

schedule = requests.get(url)
schedule_json = schedule.json()

for date in schedule_json["dates"]:
    print("==================================================")
    print("Date " + date["date"])
    print("==================================================")
    games = date["games"]
    for game in games:
        display_game(game)



# what do I want to know
# game date
# home and away teams
# team.name
# team.id
# winner - home or away 






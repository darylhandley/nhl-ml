
# get the data for one game
# https://statsapi.web.nhl.com/api/v1/game/2022020001/boxscore

import requests


class Team:
    def __init__(self, team_dict):
        self.name = team_dict["team"]["name"]
        self.score = team_dict["score"]
        self.wins = team_dict["leagueRecord"]["wins"]
        self.losses = team_dict["leagueRecord"]["losses"] + team_dict["leagueRecord"]["ot"]

    def record_for_display(self):
        return "(" + str(self.wins) + "-" + str(self.losses) + ")"

    def games_played(self):
        return self.losses + self.wins

    def win_percentage(self):
        if self.games_played() == 0:
            return 0
        else:
            return round(self.wins/self.games_played(), 3)


def process_game(game, game_date, csv_file):
    # parse teams to objects
    home = Team(game["teams"]["home"])
    away = Team(game["teams"]["away"])
    home_winner = home.score > away.score

    # we want the pre game records and not post game records so we need to subtract wins/losses
    if home_winner:
        home.wins = home.wins - 1
        away.losses = away.losses - 1
    else:
        home.losses = home.losses  - 1
        away.wins = away.wins - 1



    # output it
    # print("Game Type :" + game["gameType"])

    def display_team_game(home_or_away, team, is_winner):
        team_name_pad = 25
        winner_string = " <-- Winner" if is_winner else ""
        print(home_or_away + " :  " + team.name.ljust(team_name_pad) + " " + team.record_for_display() + " : " + str(team.score) + winner_string)

    display_team_game("Away", away, not home_winner)
    display_team_game("Home", home, home_winner)

    csv_data = [
        game_date,
        home.name,
        away.name,
        str(home.score),
        str(away.score),
        str(home.win_percentage()),
        str(away.win_percentage()),
        str(home_winner),
    ]
    csv_line = ",".join(csv_data)
    # print("Actual data row!! -> " + csv_line)
    csv_file.write(csv_line + "\n")


def filter_for_regular_season(games):
    filtered_games = []
    for game in games:
        if game["gameType"] == "R":
            filtered_games.append(game)
    return filtered_games


#########################################################
# Main
#########################################################
start_date = "2022-09-01"
end_date = "2023-03-24"
url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + start_date + "&endDate=" + end_date

schedule = requests.get(url)
schedule_json = schedule.json()

csv_file = open("game_data.csv", "w")
header_columns = [
    "date",

    "home_name",
    "away_name",

    "home_score",
    "away_score",

    "home_wins",
    "away_wins",

    "home_losses",
    "away_losses",

    "home_win_percentage",
    "away_win_percentage",

    "home_winner"
]
header = ",".join(header_columns)
csv_file.write(header + "\n")

for date in schedule_json["dates"]:

    # filter for regular season games
    # note that we filter for regular seasons here because we don't care about pre-season games for our model
    # however it seems like some regular season games are tagged as "PR" (pre-season)
    games = filter_for_regular_season(date["games"])
    if len(games) > 0:
        game_date = date['date']
        print("==================================================")
        print("Date " + date["date"])
        print("==================================================")
        game_count = 0
        for game in games:
            if game_count > 0:
                print("--------------------------------------------------")
            process_game(game, game_date, csv_file)
            game_count += 1

csv_file.close()



# what do I want to know
# game date
# home and away teams
# team.name
# team.id
# winner - home or away 






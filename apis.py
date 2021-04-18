import requests
from datetime import datetime

API_KEY = 'bbeb408e-39a6-48b6-af18-5201450084c2'
TEMP_TOKEN = '83d58bba-e966-4b00-92fb-9bd34d00c5a7'
TEMP_TOKEN_EXPIRES = 'Mon, 19 Apr 2021 14:32:38 GMT'
BASE_URL = 'https://project.trumedianetworks.com/api/'


# check to see if my temp token has expired
def is_temp_token_expired():
    today = datetime.now()
    token_expires = TEMP_TOKEN_EXPIRES
    token_expires = datetime.strptime(token_expires, '%a, %d %b %Y %H:%M:%S GMT')
    if token_expires > today:
        return False
    else:
        return True


# API to get my temp token
def get_temp_token():
    url = BASE_URL + 'token'
    headers = {'apiKey': API_KEY}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    res_json = response.json()
    if status_code != 200:
        print("ERROR: " + res_json['error'])
        return res_json['error']
    TEMP_TOKEN = res_json['token']
    TEMP_TOKEN_EXPIRES = res_json['expires']


# access api to get all players
def get_all_players():
    if is_temp_token_expired():
        get_temp_token()
    url = BASE_URL + 'nfl/players'
    headers = {'temptoken': TEMP_TOKEN}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    res_json = response.json()
    if status_code != 200:
        print("ERROR: " + res_json['error'])
        return res_json['error']
    return res_json


# acess api to get player's game stats
def get_player_games(id=None):
    if is_temp_token_expired():
        get_temp_token()
    if id == None:
        return "ERROR: No ID"
    url = BASE_URL + 'nfl/player/' + str(id)
    headers = {'temptoken': TEMP_TOKEN}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    res_json = response.json()
    if status_code != 200:
        print("ERROR: " + res_json['error'])
        return res_json['error']
    return format_game_data(res_json)


# format the game stats to things we want to return to the frontend
def format_game_data(json):
    if len(json) == 0:
        return {}
    id = json[0]['playerId']
    name = json[0]['fullName']
    playerImage = json[0]['playerImage']
    teamImage = json[0]['teamImage']
    season = json[0]['seasonYear']
    team = json[0]['team']
    team_color = "#000"
    number = 0
    age = 0

    #some hardcoded info
    if team == 'OAK':
        team = 'Oakland Raiders'
        team_color = "#000"
        number = 4
        age = 30
    elif team == 'JAX':
        team = 'Jacksonville Jaguars'
        team_color = "#006778"
        number = 5
        age = 28
    elif team == 'CLE':
        team = 'Cleveland Browns'
        team_color = "#FF3C00"
        number = 6
        age = 26

    cmpp_per_game, ypa_per_game, rypa_per_game, labels, oppImgs = [], [], [], [], []
    total_att, total_cmp, total_sacks, total_ints, total_rush_att = 0, 0, 0, 0, 0
    total_pass_yards, total_pass_tds, total_rush_yards, total_rush_tds = 0, 0, 0, 0
    for game in json:
        d = game['gameDate']
        d = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
        game['gameDate'] = datetime.strftime(d, '%a %b %d')
        game['gameTime'] = datetime.strftime(d, '%I:%M %p')

        att = game['Att']
        cmp = game['Cmp']
        yards = game['PsYds']
        ratt = game['Rush']
        ryards = game['RshYds']
        cmpp_per_game.append(round((cmp/att) * 100, 2))
        ypa_per_game.append(round(yards/att, 2))
        rypa_per_game.append(round(0 if ratt==0 else ryards/ratt, 2))

        labels.append('Week ' + str(game['week']) + ' vs ' + game['opponent'])
        oppImgs.append(game['opponentImage'])

        total_att = total_att + att
        total_cmp = total_cmp + cmp
        total_sacks = total_sacks + game['Sack']
        total_ints = total_ints + game['Int']
        total_rush_att = total_rush_att + ratt
        total_pass_yards = total_pass_yards + yards
        total_pass_tds = total_pass_tds + game['PsTD']
        total_rush_yards = total_rush_yards + ryards
        total_rush_tds = total_rush_tds + game['RshTD']

    totals = {
        'gp': len(json),
        'season': season,
        'Att': total_att,
        'Cmp': total_cmp,
        'Cmp_Percent': round((total_cmp/total_att) * 100, 2),
        'Sack': total_sacks,
        'Int': total_ints,
        'Rush': total_rush_att,
        'PsYds': total_pass_yards,
        'yds_per_att': round(total_pass_yards/total_att, 2),
        'PsTD': total_pass_tds,
        'RshYds': total_rush_yards,
        'RshTD': total_rush_tds,
        'rush_yds_per_att': round(total_rush_yards/total_rush_att, 2),
    }

    return {
        'id': id,
        'name': name,
        'playerImage': playerImage,
        'number': number,
        'age': age,
        'team': team,
        'teamImage': teamImage,
        'team_color': team_color,
        'total_stats': totals,
        'games': json,
        'cmpp_per_game': cmpp_per_game,
        'ypa_per_game': ypa_per_game,
        'rypa_per_game': rypa_per_game,
        'labels': labels,
        'oppImgs': oppImgs
    }

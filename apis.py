import requests

API_KEY = 'bbeb408e-39a6-48b6-af18-5201450084c2'

TEMP_TOKEN = '753ee2e4-2504-4309-ad78-88692b622d7e'
TEMP_TOKEN_EXPIRES = 'Sun, 18 Apr 2021 14:52:48 GMT' #TODO
BASE_URL = 'https://project.trumedianetworks.com/api/'


def get_temp_token():
    url = BASE_URL + 'token'
    headers = {'apiKey': API_KEY}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    res_json = response.json()
    if status_code != 200:
        print("ERROR: " + res_json['error'])
        return res_json['error']
    return res_json['token'], res_json['expires']


def get_all_players():
    url = BASE_URL + 'nfl/players'
    headers = {'temptoken': TEMP_TOKEN}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    res_json = response.json()
    if status_code != 200:
        print("ERROR: " + res_json['error'])
        return res_json['error']
    return res_json


def get_player_games(id=None):
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


def format_game_data(json):
    if len(json) == 0:
        return {}
    id = json[0]['playerId']
    name = json[0]['fullName']
    playerImage = json[0]['playerImage']
    teamImage = json[0]['teamImage']
    season = json[0]['seasonYear']

    cmpp_per_game, ypa_per_game, weeks_played_in = [], [], []
    total_att, total_cmp, total_sacks, total_ints, total_rush_att = 0, 0, 0, 0, 0
    total_pass_yards, total_pass_tds, total_rush_yards, total_rush_tds = 0, 0, 0, 0
    for game in json:
        att = game['Att']
        cmp = game['Cmp']
        yards = game['PsYds']
        cmpp_per_game.append(round((cmp/att) * 100, 2))
        ypa_per_game.append(round(yards/att, 2))

        weeks_played_in.append({
            'week' : game['week'],
            'opponent' : game['opponent'],
            'oppImg' : game['opponentImage']
        })

        total_att = total_att + att
        total_cmp = total_cmp + cmp
        total_sacks = total_sacks + game['Sack']
        total_ints = total_ints + game['Int']
        total_rush_att = total_rush_att + game['Rush']
        total_pass_yards = total_pass_yards + yards
        total_pass_tds = total_pass_tds + game['PsTD']
        total_rush_yards = total_rush_yards + game['RshYds']
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
        'RshTD': total_rush_tds
    }

    return {
        'id': id,
        'name': name,
        'playerImage': playerImage,
        'teamImage': teamImage,
        'total_stats': totals,
        'games': json,
        'cmpp_per_game': cmpp_per_game,
        'yds_per_game': ypa_per_game,
        'weeks_played_in': weeks_played_in
    }

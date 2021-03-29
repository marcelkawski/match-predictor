import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchpredictor.settings')
django.setup()
import requests
import datetime
import pytz
from data_providers.api_key import api_key
from games.models import Game
from clubs.models import Club


def get_next_games(headers, season_id, date_format='%Y-%m-%d', date_from=None):
    today = datetime.date.today()
    today_str = today.strftime(date_format)
    if date_from is None:
        date_from = today_str

    params = (
       ("season_id", season_id),
       ("date_from", date_from)
    )
    response = requests.get('https://app.sportdataapi.com/api/v1/soccer/matches', headers=headers, params=params)
    matches = response.json()['data']
    games = []
    for match in matches:
        game = {
            'home_team': match['home_team']['name'],
            'away_team': match['away_team']['name'],
            'date_time': match['match_start']
        }
        games.append(game)
    return games


def save_next_games_to_db(games, date_format='%Y-%m-%d %H:%M:%S'):
    for game in games:
        home_team = Club.objects.get(name=game['home_team'])
        visiting_team = Club.objects.get(name=game['away_team'])
        naive_datetime = datetime.datetime.strptime(game['date_time'], date_format)
        aware_datetime = pytz.utc.localize(naive_datetime)
        _ = Game.objects.get_or_create(home_team=home_team,
                                       visiting_team=visiting_team,
                                       date=aware_datetime)[0]


if __name__ == "__main__":
    headers = {
        "apikey": api_key
    }
    games = get_next_games(headers, 1511)
    save_next_games_to_db(games)

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchpredictor.settings')
django.setup()
import requests
import datetime
import pytz
from data_providers.api_key import headers
from data_providers.exceptions.exceptions import CurrentSeasonNotFoundError, MultipleCurrentSeasonsError
from games.models import Game
from clubs.models import Club
from seasons.models import Season


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


def get_current_season(league_name):
    try:
        return Season.objects.get(league__name=league_name, is_active=True)
    except Season.DoesNotExist:
        raise CurrentSeasonNotFoundError(league_name)
    except Season.MultipleObjectsReturned:
        raise MultipleCurrentSeasonsError(league_name)


def save_next_games_to_db(games, current_season, date_format='%Y-%m-%d %H:%M:%S'):
    for game in games:
        home_team = Club.objects.get(name=game['home_team'])
        visiting_team = Club.objects.get(name=game['away_team'])
        naive_datetime = datetime.datetime.strptime(game['date_time'], date_format)
        aware_datetime = pytz.utc.localize(naive_datetime)
        _ = Game.objects.get_or_create(home_team=home_team,
                                       visiting_team=visiting_team,
                                       date=aware_datetime,
                                       season=current_season)[0]


if __name__ == "__main__":
    league_name = 'Premier League'
    current_season = get_current_season(league_name)
    games = get_next_games(headers, current_season.api_id)
    save_next_games_to_db(games, current_season)

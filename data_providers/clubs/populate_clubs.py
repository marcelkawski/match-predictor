import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchpredictor.settings')
django.setup()
import requests
from data_providers.api_key import headers
from data_providers.exceptions.exceptions import CountryNotFoundInApiError, LeagueNotFoundInApiError, \
    CurrentSeasonNotFoundInApiError
from clubs.models import Club


def get_country_id(continent, country, headers):
    params = (
        ("continent", continent),
    )
    response = requests.get('https://app.sportdataapi.com/api/v1/soccer/countries', headers=headers, params=params)
    countries = response.json()['data']
    country_id = None
    for coun in countries.values():
        if coun['name'] == country:
            country_id = coun['country_id']
            break
    if country_id is None:
        raise CountryNotFoundInApiError(country)
    return country_id


def get_league_id(continent, country, league, headers):
    country_id = get_country_id(continent, country, headers)
    params = (
        ("country_id", country_id),
    )
    response = requests.get('https://app.sportdataapi.com/api/v1/soccer/leagues', headers=headers, params=params)
    leagues = response.json()['data']
    league_id = None
    for leag in leagues.values():
        if leag['country_id'] == country_id and leag['name'] == league:
            league_id = leag['league_id']
    if league_id is None:
        raise LeagueNotFoundInApiError(country, league)
    return league_id


def get_current_season_id(continent, country, league, headers):
    league_id = get_league_id(continent, country, league, headers)
    params = (
        ("league_id", league_id),
    )
    response = requests.get('https://app.sportdataapi.com/api/v1/soccer/seasons', headers=headers, params=params)
    seasons = response.json()['data']
    season_id = None
    for season in seasons:
        if season['is_current'] == 1:
            season_id = season['season_id']
    if season_id is None:
        raise CurrentSeasonNotFoundInApiError(country, league)
    return season_id


def get_current_season_clubs_ids(continent, country, league, headers):
    current_season_id = get_current_season_id(continent, country, league, headers)
    params = (
        ("season_id", current_season_id),
    )
    response = requests.get('https://app.sportdataapi.com/api/v1/soccer/standings', headers=headers, params=params)
    standings = response.json()['data']['standings']
    clubs_ids = []
    for standing in standings:
        clubs_ids.append(standing['team_id'])
    return clubs_ids


def get_league_current_season_clubs(continent, country, league, headers):
    current_season_clubs_ids = get_current_season_clubs_ids(continent, country, league, headers)
    clubs = []
    for club_id in current_season_clubs_ids:
        response = requests.get(f'https://app.sportdataapi.com/api/v1/soccer/teams/{club_id}', headers=headers)
        club_info = response.json()['data']
        clubs.append({
            'name': club_info['name']
        })
    return clubs


def save_clubs_to_db(clubs):
    for club in clubs:
        _ = Club.objects.get_or_create(name=club['name'])[0]


if __name__ == '__main__':
    clubs = get_league_current_season_clubs('Europe', 'England', 'Premier League', headers)
    save_clubs_to_db(clubs)

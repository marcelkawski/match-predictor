import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchpredictor.settings')
django.setup()
import requests
from data_providers.api_key import headers
from data_providers.leagues import leagues
from data_providers.exceptions.exceptions import CountryNotFoundInApiError, LeagueNotFoundInApiError, \
    CurrentSeasonNotFoundInApiError
from clubs.models import Club


def get_country_id(continent, country, _headers):
    params = (
        ("continent", continent),
    )
    response = requests.get('https://app.sportdataapi.com/api/v1/soccer/countries', headers=_headers, params=params)
    countries = response.json()['data']
    country_id = None
    for coun in countries.values():
        if coun['name'] == country:
            country_id = coun['country_id']
            break
    if country_id is None:
        raise CountryNotFoundInApiError(country)
    return country_id


def get_league_id(continent, country, _league, _headers):
    country_id = get_country_id(continent, country, _headers)
    params = (
        ("country_id", country_id),
    )
    response = requests.get('https://app.sportdataapi.com/api/v1/soccer/leagues', headers=_headers, params=params)
    _leagues = response.json()['data']
    league_id = None
    for leag in _leagues.values():
        if leag['country_id'] == country_id and leag['name'] == _league:
            league_id = leag['league_id']
    if league_id is None:
        raise LeagueNotFoundInApiError(country, _league)
    return league_id


def get_current_season_id(continent, country, _league, _headers):
    league_id = get_league_id(continent, country, _league, _headers)
    params = (
        ("league_id", league_id),
    )
    response = requests.get('https://app.sportdataapi.com/api/v1/soccer/seasons', headers=_headers, params=params)
    seasons = response.json()['data']
    season_id = None
    for season in seasons:
        if season['is_current'] == 1:
            season_id = season['season_id']
    if season_id is None:
        raise CurrentSeasonNotFoundInApiError(country, _league)
    return season_id


def get_current_season_clubs_ids(continent, country, _league, _headers):
    current_season_id = get_current_season_id(continent, country, _league, _headers)
    params = (
        ("season_id", current_season_id),
    )
    response = requests.get('https://app.sportdataapi.com/api/v1/soccer/standings', headers=_headers, params=params)
    standings = response.json()['data']['standings']
    clubs_ids = []
    for standing in standings:
        clubs_ids.append(standing['team_id'])
    return clubs_ids


def get_league_current_season_clubs(continent, country, _league, _headers):
    current_season_clubs_ids = get_current_season_clubs_ids(continent, country, _league, _headers)
    _clubs = []
    for club_id in current_season_clubs_ids:
        response = requests.get(f'https://app.sportdataapi.com/api/v1/soccer/teams/{club_id}', headers=_headers)
        club_info = response.json()['data']
        _clubs.append({
            'name': club_info['name']
        })
    return _clubs


def save_clubs_to_db(_clubs):
    for club in _clubs:
        Club.objects.get_or_create(name=club['name'])


if __name__ == '__main__':
    for league in leagues:
        clubs = get_league_current_season_clubs(league['continent'], league['country'], league['league_name'], headers)
        save_clubs_to_db(clubs)

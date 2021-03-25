import requests
import datetime
from data_providers.api_key import api_key


def get_next_matches(headers, season_id, date_format="%Y-%m-%d", date_from=None, date_to=None):
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


if __name__ == "__main__":
    headers = {
        "apikey": api_key
    }
    get_next_matches(headers, 1511)

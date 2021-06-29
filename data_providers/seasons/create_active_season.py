import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchpredictor.settings')
django.setup()

from data_providers.clubs.populate_clubs import get_current_season_id
from data_providers.api_key import headers
from data_providers.leagues import leagues
from seasons.models import Season
from leagues.models import League

if __name__ == "__main__":
    for league in leagues:
        league_obj = League.objects.get(name=league['league_name'])
        season_id = get_current_season_id(league['continent'], league['country'], league['league_name'], headers)
        Season.objects.get_or_create(league=league_obj,
                                     is_active=True,
                                     api_id=season_id)

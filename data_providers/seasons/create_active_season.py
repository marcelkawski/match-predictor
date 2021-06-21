import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchpredictor.settings')
django.setup()
from data_providers.clubs.populate_clubs import get_current_season_id
from data_providers.api_key import headers
from seasons.models import Season
from leagues.models import League


if __name__ == "__main__":
    league_name = 'Premier League'
    league = League.objects.get(name=league_name)
    season_id = get_current_season_id('Europe', 'England', league_name, headers)
    _ = Season.objects.get_or_create(league=league,
                                     is_active=True,
                                     api_id=season_id)[0]

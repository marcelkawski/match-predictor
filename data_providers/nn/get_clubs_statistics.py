import requests
from bs4 import BeautifulSoup

from data_providers.exceptions.exceptions import NoClubStatsError
from data_providers.sources import statistics_websites


def check_streak(form, result, num_matches):
    if num_matches <= len(form):
        streak = 1
        for num in range(num_matches):
            if result not in form[num]:
                streak = 0
        return streak
    return 0


def get_match_points(result):
    if result == 'W':
        return 3
    elif result == 'D':
        return 1
    else:
        return 0


def get_club_stats(club_html):
    stats = {}
    all_cols = club_html.find_all('td')
    cols = [all_cols[0]] + all_cols[3:11]
    cols = list(map(lambda c: c.text, cols))
    stats['GS'] = int(cols[5])
    stats['GC'] = int(cols[6])
    stats['P'] = int(cols[8])

    form = list(map(lambda s: s.text, club_html.find_all('span', class_=None)[1:]))
    form = form[::-1]
    last_5_games_points = 0
    for counter, result in enumerate(form):
        counter += 1
        last_5_games_points += get_match_points(result)

    stats['WinStreak3'] = check_streak(form, 'W', 3)
    stats['WinStreak5'] = check_streak(form, 'W', 5)
    stats['LossStreak3'] = check_streak(form, 'L', 3)
    stats['LossStreak5'] = check_streak(form, 'L', 5)

    stats['last_5_games_points'] = last_5_games_points
    stats['league_position'] = int(cols[0])
    stats['matches_played'] = int(cols[1])

    return stats


def get_opponents_stats(league, home_team, away_team):
    ht_stats, at_stats = None, None
    url = statistics_websites[league]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    clubs = soup.find_all('tr')[1:]
    for club in clubs:
        club_name = None
        x = club.find('abbr', class_='sp-u-abbr-on')
        if x is not None:
            club_name = x['title']
        if club_name == home_team:
            ht_stats = get_club_stats(club)
        elif club_name == away_team:
            at_stats = get_club_stats(club)
    if ht_stats is None:
        raise NoClubStatsError(home_team)
    if at_stats is None:
        raise NoClubStatsError(away_team)

    return ht_stats, at_stats


def get_match_stats(ht_stats, at_stats):
    match_stats = {'HTGS': ht_stats['GS'],
                   'ATGS': at_stats['GS'],
                   'HTGC': ht_stats['GC'],
                   'ATGC': at_stats['GC'],
                   'HTP': ht_stats['P'],
                   'ATP': at_stats['P'],
                   'HTWinStreak3': ht_stats['WinStreak3'],
                   'HTWinStreak5': ht_stats['WinStreak5'],
                   'HTLossStreak3': ht_stats['LossStreak3'],
                   'HTLossStreak5': ht_stats['LossStreak5'],
                   'ATWinStreak3': at_stats['WinStreak3'],
                   'ATWinStreak5': at_stats['WinStreak5'],
                   'ATLossStreak3': at_stats['LossStreak3'],
                   'ATLossStreak5': at_stats['LossStreak5'],
                   'HTGD': ht_stats['GS'] - ht_stats['GC'],
                   'ATGD': at_stats['GS'] - at_stats['GC'],
                   'DiffPts': ht_stats['P'] - at_stats['P'],
                   'DiffFormPts': ht_stats['last_5_games_points'] - at_stats['last_5_games_points'],
                   'DiffLP': ht_stats['league_position'] - at_stats['league_position']}

    return match_stats, ht_stats['matches_played'], at_stats['matches_played']


def normalize_match_stats(match_stats, ht_mp, at_mp):  # home/away team matches played
    match_stats['HTGS'] /= ht_mp
    match_stats['ATGS'] /= at_mp
    match_stats['HTGC'] /= ht_mp
    match_stats['ATGC'] /= at_mp
    match_stats['HTP'] /= ht_mp
    match_stats['ATP'] /= at_mp
    match_stats['HTGD'] /= ht_mp
    match_stats['ATGD'] /= at_mp
    match_stats['DiffPts'] /= ht_mp
    return match_stats

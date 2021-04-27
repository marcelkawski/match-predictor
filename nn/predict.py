import torch
import requests
import numpy as np
from bs4 import BeautifulSoup
from nn.train import MatchPredictor
from nn.exceptions import NoClubStatsError


websites = {
    'LaLiga': 'https://www.skysports.com/la-liga-table',
    'Premier League': 'https://www.skysports.com/premier-league-table'
}


def check_streak(form, result, num_matches):
    if num_matches <= len(form):
        streak = 1
        for num in range(num_matches):
            if result not in form[num]:
                streak = 0
        return streak
    return 0


def get_match_points(match):
    if 'win' in match:
        return 3
    elif 'draw' in match:
        return 1
    else:
        return 0


def get_club_stats(club_html):
    stats = {}
    cols = list(map(lambda c: c.text, club_html.find_all('td', class_='standing-table__cell')))
    stats['GS'] = int(cols[6])
    stats['GC'] = int(cols[7])
    stats['P'] = int(cols[9])

    form = list(map(lambda m: str(m), club_html.find_all('span', class_='standing-table__form-cell')[:-6:-1]))
    last_5_games_points = 0
    for counter, match in enumerate(form):
        counter += 1
        last_5_games_points += get_match_points(match)
        result = None
        if counter != 1:
            if 'win' in match:
                result = 0, 0, 0, 1
            elif 'draw' in match:
                result = 1, 0, 0, 0
            elif 'loss' in match:
                result = 0, 1, 0, 0
            stats[f'M{counter}.0'], stats[f'M{counter}.1'], stats[f'M{counter}.2'], stats[f'M{counter}.3'] = result
        else:
            if 'win' in match:
                result = 0, 0, 1
            elif 'draw' in match:
                result = 1, 0, 0
            elif 'loss' in match:
                result = 0, 1, 0
            stats[f'M{counter}.1'], stats[f'M{counter}.2'], stats[f'M{counter}.3'] = result

    stats['WinStreak3'] = check_streak(form, 'win', 3)
    stats['WinStreak5'] = check_streak(form, 'win', 5)
    stats['LossStreak3'] = check_streak(form, 'loss', 3)
    stats['LossStreak5'] = check_streak(form, 'loss', 5)

    stats['last_5_games_points'] = last_5_games_points
    stats['league_position'] = int(cols[0])
    stats['matches_played'] = int(cols[2])

    return stats


def get_opponents_stats(league, home_team, away_team):
    ht_stats, at_stats = None, None
    url = websites[league]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    clubs = soup.find_all('tr', class_='standing-table__row')[1:]
    for club in clubs:
        club_name = club.find('td', class_='standing-table__cell--name')['data-long-name']
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
                   'ATP': at_stats['P']}

    for i in range(1, 6):
        if i != 1:
            for j in range(4):
                match_stats[f'HM{i}.{j}'] = ht_stats[f'M{i}.{j}']
                match_stats[f'AM{i}.{j}'] = at_stats[f'M{i}.{j}']
        else:
            for j in range(1, 4):
                match_stats[f'HM{i}.{j}'] = ht_stats[f'M{i}.{j}']
                match_stats[f'AM{i}.{j}'] = at_stats[f'M{i}.{j}']

    match_stats['HTWinStreak3'] = ht_stats['WinStreak3']
    match_stats['HTWinStreak5'] = ht_stats['WinStreak5']
    match_stats['HTLossStreak3'] = ht_stats['LossStreak3']
    match_stats['HTLossStreak5'] = ht_stats['LossStreak5']

    match_stats['ATWinStreak3'] = at_stats['WinStreak3']
    match_stats['ATWinStreak5'] = at_stats['WinStreak5']
    match_stats['ATLossStreak3'] = at_stats['LossStreak3']
    match_stats['ATLossStreak5'] = at_stats['LossStreak5']

    match_stats['HTGD'] = ht_stats['GS'] - ht_stats['GC']
    match_stats['ATGD'] = at_stats['GS'] - at_stats['GC']

    match_stats['DiffPts'] = ht_stats['P'] - at_stats['P']
    match_stats['DiffFormPts'] = ht_stats['last_5_games_points'] - at_stats['last_5_games_points']
    match_stats['DiffLP'] = ht_stats['league_position'] - at_stats['league_position']

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


def predict_match(league, home_team, away_team):
    home_team_stats, away_team_stats = get_opponents_stats(league, home_team, away_team)
    match_statistics, ht_matches_played, at_matches_played = get_match_stats(home_team_stats, away_team_stats)
    match_statistics = normalize_match_stats(match_statistics, ht_matches_played, at_matches_played)

    match_statistics = np.array(list(match_statistics.values()))
    match_statistics = torch.from_numpy(match_statistics)

    model = MatchPredictor().double()
    model.load_state_dict(torch.load("model.pth"))
    model.eval()

    with torch.no_grad():
        pred = model(match_statistics)

    return pred

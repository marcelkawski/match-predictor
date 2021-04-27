import torch
import requests
from requests_html import HTMLSession, AsyncHTMLSession
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


def get_club_stats(club_html):
    # print(club_html)
    stats = {}
    cols = list(map(lambda c: c.text, club_html.find_all('td', class_='standing-table__cell')))
    # print(cols)
    stats['GS'] = cols[6]
    stats['GC'] = cols[7]
    stats['P'] = cols[9]

    form = list(map(lambda m: str(m), club_html.find_all('span', class_='standing-table__form-cell')[:-6:-1]))
    for counter, match in enumerate(form):
        counter += 1
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

    stats['WinStreak3'], stats['WinStreak5'], stats['LossStreak3'], stats['LossStreak5'] = 0, 0, 0, 0
    if len(form) >= 3:
        pass

    print(stats)


def get_stats(league, home_team, away_team):
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
    # if ht_stats is None:
    #     raise NoClubStatsError(home_team)
    # if at_stats is None:
    #     raise NoClubStatsError(away_team)
    return ht_stats, at_stats


# def predict_match(stats):
#     with torch.no_grad():
#         pred = model(stats)
#         prediction = pred[0].argmax(0)
#     return prediction


if __name__ == '__main__':
    get_stats('LaLiga', 'Barcelona', 'Atletico Madrid')
    # model = MatchPredictor()
    # model.load_state_dict(torch.load("model.pth"))
    # model.eval()
    # stats = get_match_stats()
    # match_result = predict_match(stats)

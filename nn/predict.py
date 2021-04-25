import torch
import requests
from requests_html import HTMLSession, AsyncHTMLSession
from bs4 import BeautifulSoup
from nn.train import MatchPredictor


websites = {
    'LaLiga': 'https://www.skysports.com/la-liga-table',
    'Premier League': 'https://www.skysports.com/premier-league-table'
}


def get_stats(league, home_team, away_team):
    url = websites[league]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    clubs = soup.find_all('tr', class_='standing-table__row')[1:]
    print(clubs[0])
    for club in clubs:
        pass
    # ht_stats = get_club_stats(home_team, page)
    # at_stats = get_club_stats(away_team, page)


# def predict_match(stats):
#     with torch.no_grad():
#         pred = model(stats)
#         prediction = pred[0].argmax(0)
#     return prediction


if __name__ == '__main__':
    get_stats('LaLiga', 'FC Barcelona', 'Atletico Madrid')
    # model = MatchPredictor()
    # model.load_state_dict(torch.load("model.pth"))
    # model.eval()
    # stats = get_match_stats()
    # match_result = predict_match(stats)

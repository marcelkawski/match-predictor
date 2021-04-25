import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchpredictor.settings')
django.setup()
import requests


websites = {
    'LaLiga': 'https://www.flashscore.com/standings/trCLzEsJ/I58n6IRP/#table/overall',
    'Premier League': 'https://www.flashscore.com/standings/AJuiuwWt/zTRyeuJg/#table/overall'
}
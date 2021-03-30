from django.views import generic
from clubs.models import Club


class ClubDetailView(generic.DetailView):
    model = Club

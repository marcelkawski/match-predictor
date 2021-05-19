from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from clubs.models import Club, ClubFan


class ClubDetailView(generic.DetailView):
    model = Club


class AddClubToFavsView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('clubs:club_details', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        club = get_object_or_404(Club, slug=self.kwargs.get('slug'))
        try:
            ClubFan.objects.create(user=self.request.user, club=club)
        except IntegrityError:
            messages.warning(self.request, f"You are already a fan of the {club.name}")
        else:
            messages.success(self.request, f"You are now a fan of the {club.name}.")

        return super().get(request, *args, **kwargs)


class DeleteClubFromFavsView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('clubs:club_details', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        club = get_object_or_404(Club, slug=self.kwargs.get('slug'))
        try:
            club_fan = ClubFan.objects.filter(
                user=self.request.user,
                club__slug=self.kwargs.get('slug')).get()
        except ClubFan.DoesNotExist:
            messages.warning(self.request, f"You are not a fan of the {club.name}.")
        else:
            club_fan.delete()
            messages.success(self.request, f"You have deleted the {club.name} from your favourite clubs.")

        return super().get(request, *args, **kwargs)


class DeleteClubFromFavsInMyClubsView(DeleteClubFromFavsView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('clubs:user_fav_clubs', kwargs={'username': self.kwargs.get('username')})


class FavoriteClubsView(LoginRequiredMixin, generic.ListView):
    model = ClubFan
    template_name = 'clubs/user_fav_clubs_list.html'


class ClubsRankingView(generic.ListView):
    model = Club
    template_name = 'clubs/clubs_ranking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clubs = list(Club.objects.all().order_by('-fans'))
        clubs_fans = {club: club.fans.count() for club in clubs}
        
        r = {key: rank for rank, key in enumerate(sorted(set(clubs_fans.values()), reverse=True), 1)}
        ranking = {k: r[v] for k, v in clubs_fans.items()}
        
        clubs_ranking = {}
        for club, position in ranking.items():
            if position in clubs_ranking:
                clubs_ranking[position].append(club)
            else:
                clubs_ranking[position] = [club]

        clubs_ranking_items = clubs_ranking.items()
        clubs_ranking = dict(sorted(clubs_ranking_items))

        context['clubs_ranking'] = clubs_ranking
        return context

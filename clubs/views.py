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
        return reverse('clubs:user_fav_clubs')


class FavoriteClubsView(LoginRequiredMixin, generic.ListView):
    model = ClubFan
    # select_related = ('user', 'club')
    template_name = 'clubs/user_fav_clubs_list.html'

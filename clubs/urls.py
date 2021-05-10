from django.urls import path
from . import views


app_name = 'clubs'

urlpatterns = [
    path('details/<slug>/', views.ClubDetailView.as_view(), name='club_details'),
    path('add-to-favs/<slug>/', views.AddClubToFavsView.as_view(), name='add_club_to_favs'),
    path('delete-from-favs/<slug>/', views.DeleteClubFromFavsView.as_view(), name='delete_club_from_favs'),
    path('delete-from-favs-imc/<slug>/', views.DeleteClubFromFavsInMyClubsView.as_view(), name='delete_club_from_favs-imc'),
    path('favs/<username>/', views.FavoriteClubsView.as_view(), name='user_fav_clubs'),
    path('clubs-ranking/', views.ClubsRankingView.as_view(), name='clubs_ranking')
]

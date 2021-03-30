from django.urls import path
from . import views


app_name = 'clubs'

urlpatterns = [
    path('<int:pk>/', views.ClubDetailView.as_view(), name='club_details'),
]

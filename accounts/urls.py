from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views
from accounts.tokens import user_tokenizer
from matchpredictor import settings


app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('confirm-registration/<str:user_id>/<str:token>/', views.ConfirmRegistrationView.as_view(),
         name='confirm_registration'),
    path(
        'reset-password/',
        auth_views.PasswordResetView.as_view(
          template_name='accounts/reset_password.html',
          html_email_template_name='accounts/reset_password_email.html',
          success_url=settings.LOGIN_URL,
          token_generator=user_tokenizer),
        name='reset_password'
      ),
]
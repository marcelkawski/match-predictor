from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from accounts import views
from accounts.tokens import user_tokenizer


app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('confirm-registration/<str:user_id>/<str:token>/', views.ConfirmRegistrationView.as_view(),
         name='confirm_registration'),
    path('reset-pwd-email-sent', views.ResetPwdEmailSent.as_view(), name='reset_pwd_email_sent'),
    path('reset-pwd-completed', views.ResetPwdCompleted.as_view(), name='reset_pwd_completed'),
    path(
        'reset-pwd/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/reset_pwd.html',
            email_template_name='accounts/reset_pwd_email.html',
            html_email_template_name='accounts/reset_pwd_email.html',
            success_url=reverse_lazy('accounts:reset_pwd_email_sent'),
            token_generator=user_tokenizer),
        name='reset_pwd'
      ),
    path(
        'reset-pwd-conf/<str:uidb64>/<str:token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/pwd_reset_conf.html',
            post_reset_login_backend='django.contrib.auth.backends.ModelBackend',
            token_generator=user_tokenizer,
            success_url=reverse_lazy('accounts:reset_pwd_completed')),
        name='reset_pwd_conf'
      ),
]

from django.views import View
from django.views.generic import CreateView, DetailView
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.shortcuts import redirect
from accounts.tokens import user_tokenizer
from accounts.forms import CreateUserForm, ChangeUsernameForm

UserModel = get_user_model()


class SignUpView(CreateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/signup.html', {'form': CreateUserForm()})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            token = user_tokenizer.make_token(user)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            domain = get_current_site(request).domain
            url = 'http://' + domain + reverse('accounts:confirm_registration', kwargs={'user_id': user_id,
                                                                                        'token': token})
            message = get_template('accounts/registration_email.html').render({
                'confirmation_url': url
            })
            mail = EmailMessage('MatchPredictor Email Confirmation', message, to=[user.email],
                                from_email=settings.EMAIL_HOST_USER)
            mail.content_subtype = 'html'
            mail.send()

            return render(request, 'accounts/conf_email_info.html', {
                'form': AuthenticationForm(),
                'user_email': user.email,
            })

        return render(request, 'accounts/signup.html', {'form': form})


class ConfirmRegistrationView(View):
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))
        user = User.objects.get(pk=user_id)
        context = {
            'form': AuthenticationForm(),
        }
        if user and user_tokenizer.check_token(user, token):
            user.is_active = True
            user.save()
        return render(request, 'accounts/registration_conf.html', context)


class ResetPwdEmailSent(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/reset_pwd_info.html')


class ResetPwdCompleted(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/reset_pwd_completed.html')


class UserSettingsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/user_settings.html')


def change_username(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, instance=request.user)
        args = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('accounts:user_settings')
        else:
            return render(request, 'accounts/change_username.html', args)
    else:
        form = ChangeUsernameForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_username.html', args)

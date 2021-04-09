from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, reverse
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.forms import AuthenticationForm
from accounts.tokens import user_tokenizer
from accounts.forms import CreateUserForm

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
                'message': f'A confirmation email has been sent to {user.email}. Please click the link we sent to '
                           f'finish the registration.'
            })

        return render(request, 'accounts/signup.html', {'form': form})


class ConfirmRegistrationView(View):
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))
        user = User.objects.get(pk=user_id)
        context = {
            'form': AuthenticationForm(),
            'message': 'Registration complete. Please log in.',
        }
        if user and user_tokenizer.check_token(user, token):
            user.is_active = True
            user.save()

        return render(request, 'accounts/registration_conf.html', context)

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from accounts.tokens import user_tokenizer
from accounts.forms import CreateUserForm

UserModel = get_user_model()


class SignUpView(View):
    # form_class = CreateUserForm
    # success_url = reverse_lazy('accounts:login')
    # template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/signup.html', {'form': CreateUserForm()})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            print(user.is_active)
            user.save()
            token = user_tokenizer.make_token(user)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            url = 'http://localhost:8000' + reverse('accounts:confirm_registration', kwargs={'user_id': user_id,
                                                                                             'token': token})
            message = get_template('accounts/registration_email.html').render({
                'confirm_url': url
            })
            mail = EmailMessage('MatchPredictor Email Confirmation', message, to=[user.email],
                                from_email=settings.EMAIL_HOST_USER)
            mail.content_subtype = 'html'
            mail.send()

            return render(request, 'accounts/login.html', {
                'form': AuthenticationForm(),
                'message': f'A confirmation email has been sent to {user.email}. Please confirm to finish registering'
            })

        return render(request, 'accounts/signup.html', {'form': form})


# class LoginView(View):
#     def get(self, request):
#         return render(request, 'accounts/login.html', {'form':  AuthenticationForm()})
#
#     def post(self, request):
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             try:
#                 form.clean()
#             except ValidationError:
#                 return render(
#                     request,
#                     'accounts/login.html',
#                     {'form': form, 'invalid_creds': True}
#                 )
#
#             user = form.get_user()
#             print('Valid:')
#             print(user.is_valid)
#
#             login(request, form.get_user())
#             # return redirect(reverse(''))
#         return render(request, 'accounts/login.html', {'form': form})


class ConfirmRegistrationView(View):
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))
        user = User.objects.get(pk=user_id)
        context = {
            'form': AuthenticationForm(),
            'message': 'Registration confirmation required. Please click "reset password" to generate a new '
                       'confirmation email.'
        }
        if user and user_tokenizer.check_token(user, token):
            user.is_active = True
            print(user.is_active)
            user.save()
            context['message'] = 'Registration complete. Please log in.'

        return render(request, 'accounts/login.html', context)

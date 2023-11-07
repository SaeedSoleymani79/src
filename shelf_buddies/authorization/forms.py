from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import Userprofile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


User = get_user_model()

class registerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class imgForm(forms.Form):
    picture = forms.ImageField()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)

class UserUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ('profile_image', 'profile_bio')  # Add 'bio' here


class CustomChangePasswordForm(SetPasswordForm):
    old_password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Your old password was entered incorrectly. Please enter it again.')
        return old_password
    
class CustomPasswordResetForm(PasswordResetForm):
    email = None
    identifier = forms.CharField(max_length=254)

    def clean_identifier(self):
        identifier = self.cleaned_data['identifier']
        if '@' in identifier:
            # User entered email
            if not User.objects.filter(email__iexact=identifier).exists():
                raise forms.ValidationError("There is no user registered with the specified email.")
        else:
            # User entered a username
            if not User.objects.filter(username__iexact=identifier).exists():
                raise forms.ValidationError("There is no user registered with the speciifed username.")
        return identifier
    
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=None,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        identifier = self.cleaned_data["identifier"]
        for user in self.get_users(identifier):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user.email, html_email_template_name=html_email_template_name,
            )
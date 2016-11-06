from django.contrib.auth.models import User
from master.models import Nieuwsbrief
from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email':  forms.TextInput(attrs={'class': 'w3-input w3-border w3-round-xlarge email-field form-control', 'style':'outline:none;'}),
            'password': forms.PasswordInput(attrs={'class': 'w3-input w3-border w3-round-xlarge password-field form-control', 'style':'outline:none;'}),
        }


class VerkoperForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round-large partner-field', 'placeholder' : 'voornaam'}),
            'last_name': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round-large partner-field', 'placeholder' : 'achternaam'}),
            'email': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round-large partner-field', 'placeholder' : 'email'}),
        }

class ContactForm(forms.Form):

        contact_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'w3-input', 'style': 'text-align:center;font-size:1.4em;'}))
        contact_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'w3-input', 'style': 'text-align:center;font-size:1.4em;'}))
        contact_subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'w3-input', 'style': 'text-align:center;font-size:1.4em;'}))
        contact_message = forms.CharField(widget=forms.Textarea(attrs={'style': 'width:100%;max-height: 15%;'}))
        captcha = NoReCaptchaField(label="")

class NieuwsbriefForm(forms.ModelForm):

    class Meta:
        model = Nieuwsbrief
        fields = ['email']
        widgets = {'email': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round-large partner-field', 'placeholder' :'email'})}
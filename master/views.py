#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os, json, functools, datetime, uuid
from .models import User, Pand, PandHitCount, Status, TypeHuis, Criteria, \
    PandEigenschap, Staat, PandCriteria, Nieuwsbrief, DynamicPageContent, \
    DynamicPageContent_EN, DynamicPageContent_FR, PandBezichtiging, Eigenschap, \
    PandDocument
from master.forms import LoginForm, VerkoperForm, NieuwsbriefForm, ContactForm
from django.views.generic import View, TemplateView
from django.views import generic
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ipware.ip import get_ip
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.translation import get_language
from django.core import serializers
from django.core.urlresolvers import reverse
from itertools import chain
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.template.response import TemplateResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.utils.encoding import smart_str
from django.views.decorators.vary import vary_on_headers

LOGIN_PASSWORD_WRONG_TEXT = 'Email/Wachtwoord zijn niet correct!'
LOGIN_NOT_FOUND_TEXT = 'Email/Wachtwoord zijn niet correct!'
LOGIN_INVALID_FORM_TEXT = 'Velden zijn niet correct ingevuld!'


class PreSearch(View):

    def post(self, request):
        print(request)
        return JsonResponse({'data': 'post success'})


def deprecate_current_app(func):
    """
    Handle deprecation of the current_app parameter of the views.
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        if 'current_app' in kwargs:
            warnings.warn(
                "Passing `current_app` as a keyword argument is deprecated. "
                "Instead the caller of `{0}` should set "
                "`request.current_app`.".format(func.__name__),
                RemovedInDjango20Warning
            )
            current_app = kwargs.pop('current_app')
            request = kwargs.get('request', None)
            if request and current_app is not None:
                request.current_app = current_app
        return func(*args, **kwargs)

    return inner


@deprecate_current_app
@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   extra_context=None,
                   html_email_template_name=None,
                   extra_email_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
                'extra_email_context': extra_email_context,
            }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 1.10.",
                    RemovedInDjango110Warning, 3
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
        context = LoadFooter.get_context(LoadFooter)
    context['form'] = form
    context['title'] = 'Password reset'
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@deprecate_current_app
def password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        extra_context=None):
    context = LoadFooter.get_context(LoadFooter)
    context['title'] = 'Password reset'
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
@deprecate_current_app
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
        context = LoadFooter.get_context(LoadFooter)
    context['form'] = form
    context['title'] = 'Password reset'
    context['validlink'] = validlink
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@deprecate_current_app
def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            extra_context=None):
    context = LoadFooter.get_context(LoadFooter)
    context['login_url'] = resolve_url(settings.LOGIN_URL)
    context['title'] = 'Password reset'
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


class MijnPanden(View):
    def get(self, request):
        if request.user.is_authenticated():
            panden = Pand.objects.filter(user=request.user)
            bezichtigingen = PandBezichtiging.objects.filter(pand__in=panden)
            context = LoadFooter.get_context(LoadFooter)
            context['bezichtiging'] = bezichtigingen
            context['panden'] = panden
            return render(request, 'master/mijn-panden.html', context)
        else:
            redirect('index')


class loadAdvancedSearch():

    def loop_add_to_array(self, array, language):
        new_array = []
        for v in array:
            if language == 'fr':
                new_array.append(v.naam_fr)
            elif language == 'en':
                new_array.append(v.naam_en)
            else:
                new_array.append(v.naam)
        return new_array

    def get_context(self, context):
        status = Status.objects.all()
        typehuis = TypeHuis.objects.all()
        criteria = Criteria.objects.all()
        staat = Staat.objects.all()
        array_type = self.loop_add_to_array(typehuis, get_language())
        array_status = self.loop_add_to_array(status, get_language())
        array_criteria = self.loop_add_to_array(criteria, get_language())
        array_staat = self.loop_add_to_array(staat, get_language())
        context['status'] = array_status
        context['typehuis'] = array_type
        context['criteria'] = array_criteria
        context['staat'] = array_staat
        return context

class LoadFooter():
    @staticmethod
    def get_context(self):
        if get_language() == 'fr':
            footer_biv = DynamicPageContent_FR.objects.filter(identifier__icontains='footer_biv').first()
            footer_tel = DynamicPageContent_FR.objects.filter(identifier__icontains='footer_tel').first()
            footer_adres = DynamicPageContent_FR.objects.filter(identifier__icontains='footer_adres').first()
            footer_email = DynamicPageContent_FR.objects.filter(identifier__icontains='footer_email').first()
        elif get_language() == 'en':
            footer_biv = DynamicPageContent_EN.objects.filter(identifier__icontains='footer_biv').first()
            footer_tel = DynamicPageContent_EN.objects.filter(identifier__icontains='footer_tel').first()
            footer_adres = DynamicPageContent_EN.objects.filter(identifier__icontains='footer_adres').first()
            footer_email = DynamicPageContent_EN.objects.filter(identifier__icontains='footer_email').first()
        else:
            footer_biv = DynamicPageContent.objects.filter(identifier__icontains='footer_biv').first()
            footer_tel = DynamicPageContent.objects.filter(identifier__icontains='footer_tel').first()
            footer_adres = DynamicPageContent.objects.filter(identifier__icontains='footer_adres').first()
            footer_email = DynamicPageContent.objects.filter(identifier__icontains='footer_email').first()
        context = {
            'footer_biv': footer_biv,
            'footer_tel': footer_tel,
            'footer_adres': footer_adres,
            'footer_email': footer_email
        }
        context = loadAdvancedSearch().get_context(context)
        return context

    @staticmethod
    def load_content(self):
        if get_language() == 'fr':
            footer_biv = DynamicPageContent_FR.objects.filter(identifier__icontains='footer_biv').first()
            footer_tel = DynamicPageContent_FR.objects.filter(identifier__icontains='footer_tel').first()
            footer_adres = DynamicPageContent_FR.objects.filter(identifier__icontains='footer_adres').first()
            footer_email = DynamicPageContent_FR.objects.filter(identifier__icontains='footer_email').first()
        elif get_language() == 'en':
            footer_biv = DynamicPageContent_EN.objects.filter(identifier__icontains='footer_biv').first()
            footer_tel = DynamicPageContent_EN.objects.filter(identifier__icontains='footer_tel').first()
            footer_adres = DynamicPageContent_EN.objects.filter(identifier__icontains='footer_adres').first()
            footer_email = DynamicPageContent_EN.objects.filter(identifier__icontains='footer_email').first()
        else:
            footer_biv = DynamicPageContent.objects.filter(identifier__icontains='footer_biv').first()
            footer_tel = DynamicPageContent.objects.filter(identifier__icontains='footer_tel').first()
            footer_adres = DynamicPageContent.objects.filter(identifier__icontains='footer_adres').first()
            footer_email = DynamicPageContent.objects.filter(identifier__icontains='footer_email').first()
        object = [footer_biv, footer_tel, footer_adres, footer_email]
        return object

    def __init__(self):
        return None


class SiteMap(View):
    def get(self, request):
        context = LoadFooter.get_context(LoadFooter)
        return render(request, 'master/sitemap.html', context)


class Disclaimer(View):
    def get(self, request):
        context = LoadFooter.get_context(LoadFooter)
        return render(request, 'master/disclaimer.html', context)


class PrivacyBeleid(View):
    def get(self, request):
        context = LoadFooter.get_context(LoadFooter)
        return render(request, 'master/privacybeleid.html', context)


class AdminSupportTicket(View):
    def post(self, request):
        onderwerp = request.POST.get('onderwerp', '')
        bericht = request.POST.get('bericht', '')
        email = EmailMessage(
            onderwerp,
            bericht,
            "Via Sofie" + '',
            [settings.EMAIL_HOST_USER],
            ['sami.c@hotmail.be'])
        email.send()
        return JsonResponse({'success': 'Data is handled correctly'})


def change_password(request):
    template_response = views.password_change(request)
    # Do something with `template_response`
    return template_response


def contact_view(request):
    form_class = ContactForm
    context = LoadFooter.get_context(LoadFooter)
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            name = request.POST.get('name', '')
            subject = request.POST.get('subject', '')
            email = request.POST.get('email', '')
            content = request.POST.get('message', '')
            message = "Nieuwe contactaanvraag van: " + name + "\n" + "Email adres: " + email + "\n" + "Vraag: " + content
            email = EmailMessage(
                "Nieuwe contact aanvraag",
                message,
                "Via Sofie" + '',
                [settings.EMAIL_HOST_USER],
                headers={'Reply-To': email})
            email.send()
            return render(request, 'master/contact-success.html', context)
        else:
            # errors = form.errors
            #  return HttpResponse(json.dumps(errors))
            context['form'] = form
            return render(request, 'master/contact.html', context)
    context['form'] = form_class
    return render(request, 'master/contact.html', context)


class SendNieuwsbrief(View):
    def get(self, request):
        if request.user.is_superuser:
            context = LoadFooter.get_context(LoadFooter)
            return render(request, 'master/verstuur-nieuwsbrief.html', context)
        else:
            return redirect('index')

    def post(self, request):
        if request.user.is_superuser:
            file = request.POST.get('my-upload-file', request.FILES)
            subject = request.POST.get('newsletter-subject', '')
            message = request.POST.get('newsletter-message', '')
            contacten = Nieuwsbrief.objects.filter(actief=True)
            print("contacten : " + str(contacten))
            if file in [None, '']:
                return render(request, 'master/verstuur-nieuwsbrief.html', {'message': 'Er is iets fout gegaan!'})
            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                contacten)
            email.attach('test.pdf', request.FILES['my-upload-file'].read(), 'application/pdf')
            email.send()
            context = LoadFooter.get_context(LoadFooter)
            context['message'] = 'Nieuwsbrief is succesvol naar alle lezers verstuurd!'
        return render(request, 'master/verstuur-nieuwsbrief.html', context)


class RegisterNieuwsbrief(View):
    form_class = NieuwsbriefForm
    template_name = 'master/registreer-nieuwsbrief.html'

    def post(self, request):
        email = request.POST.get('cd-email')
        print(email)
        context = LoadFooter.get_context(LoadFooter)
        if email not in [None, '']:
            if not Nieuwsbrief.objects.filter(email=email).exists():
                activate_code = str(uuid.uuid4())
                nieuwsbrieflid = Nieuwsbrief.objects.create(email=email, activate_code=activate_code)
                nieuwsbrieflid.save()
                subject = "inschrijving nieuwsbrief"
                html_content = '<center><div style="background-color:#0d3532; border:14px solid black; ' \
                               'color:whitesmoke;padding:40px;"><h1 style="text-align:center;color:darkseagreen;">' \
                               'Welkom bij VIA SOFIE!</h1>' + \
                               '<p style="text-align:center">Klik de link om je actief te stellen voor de nieuwsbrief' + \
                               'van VIA SOFIE</p> <center><a href="' + \
                               str(request.build_absolute_uri(reverse('index'))) + \
                               'nieuwsbrief/activate/' + activate_code + '">Activeer nieuwsbrief</a></center>' + \
                               '<p></p>' \
                               '<h2 style="text-align:center" >Sofie</h2>' + \
                               '<img src="static/master/img/base/logo.png" width="60px" height="60px"/>' \
                               '</div></center>'
                msg = EmailMultiAlternatives(subject, 'test', settings.EMAIL_HOST_USER, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.mixed_subtype = 'related'
                """test = msg.attach_file('http://localhost:8000' + settings.STATIC_URL + 'master/img/base/logo.png')
                fp = open(test, 'rb')
                msg_img = MIMEImage(fp.read())
                fp.close()
                msg_img.add_header('Content-ID', '<{}>'.format(f))
                msg.attach(msg_img)"""
                msg.send()
                context['success'] = 'mail is gestuurd naar ' + str(
                    email) + ' klik op de link om je account te activeren voor nieuwsbrieven.'
                return JsonResponse({'message-success': 'mail is gestuurd naar ' + str(
                    email) + ' klik op de link om je account te activeren voor nieuwsbrieven.'})
            else:
                return JsonResponse({'message-error': 'Dit email is al reeds geregistreerd!'})
        else:
            context['form'] = form
            return JsonResponse({'message-error': 'Geen geldig email!'})

    def get(self, request):
        context = LoadFooter.get_context(LoadFooter)
        context['form'] = self.form_class
        print(request.build_absolute_uri(reverse('index')))
        return render(request, 'master/registreer-nieuwsbrief.html', context)


class ActiveerNieuwsbrief(generic.DetailView):
    model = Nieuwsbrief
    template_name = 'master/activeer-nieuwsbrief.html'
    context_object_name = 'nieuwsbrief'

    def get_object(self):
        object = Nieuwsbrief.objects.filter(actief=False, activate_code=self.kwargs['activate_code'])
        if len(object) > 0:
            object[0].actief = True
            object[0].save()
        else:
            object = '1'
        return object

    def render_to_response(self, context, **response_kwargs):
        response = super(ActiveerNieuwsbrief, self).render_to_response(context, **response_kwargs)
        context['footer_biv'] = LoadFooter.load_content(LoadFooter)[0]
        context['footer_tel'] = LoadFooter.load_content(LoadFooter)[1]
        context['footer_adres'] = LoadFooter.load_content(LoadFooter)[2]
        context['footer_email'] = LoadFooter.load_content(LoadFooter)[3]
        return response


class Pand_Main():
    def handle_post_request_advanced(self, request, status):
        gemeente = ''
        criteria_v = []

        # Values from form fields
        status = request.POST.get('statuspicker')
        typehuis = request.POST.get('housetype')
        staat = request.POST.get('property')
        locatie = request.POST.get('location').split()
        criteria = Criteria.objects.all()
        min_prijs = request.POST.get('price-min')
        max_prijs = request.POST.get('price-max')
        min_opp = request.POST.get('size-min')
        max_opp = request.POST.get('size-max')
        bouwjaar = request.POST.get('min-build')
        min_slaapkamers = request.POST.get('amt-slaapkamers')
        min_badkamers = request.POST.get('amt-badkamers')
        ref_number = request.POST.get('ref-number')
        print("oppervlakte : " + str(min_opp))
        print("oppervlakte : " + str(max_opp))
        print("fsdjkfsdjmkfjmsd " + str(staat))
        # iterate over every criteria that the user selected
        # They can then be used to check for pand criteria
        for c in criteria:
            if request.POST.get(c.naam) is not None:
                criteria_v.append(request.POST.get(c.naam))

        # Safety checks
        if status in [None, '']:
            status = ''
        if typehuis in [None, '']:
            typehuis = ''
        if locatie in [None, '']:
            locatie = ''
        if bouwjaar in [None, ''] or bouwjaar.isdigit() == False:
            bouwjaar = 0
        if staat in [None, '']:
            staat = ''
        if min_slaapkamers in [None, ''] or min_slaapkamers.isdigit() == False:
            min_slaapkamers = 0
        if min_badkamers in [None, ''] or min_badkamers.isdigit():
            min_badkamers = 0
        if ref_number in [None, '']:
            ref_number = ''
        if len(locatie) > 0:
            gemeente = locatie[1]
        if min_prijs in [None, ''] or min_prijs.isdigit() == False:
            min_prijs = 0
        if max_prijs in [None, ''] or max_prijs.isdigit() == False:
            max_prijs = 2147000000
        # Complex queries
        criteria_query = PandCriteria.objects.values_list('pand', flat=True) \
            .filter(criteria__naam__in=criteria_v)
        aantal_slaapkamers_criteria_query = PandCriteria.objects.values_list('pand', flat=True) \
            .filter(criteria__naam__icontains='slaapkamers', aantal__gte=min_slaapkamers)
        aantal_badkamers_criteria_query = PandCriteria.objects.values_list('pand', flat=True) \
            .filter(criteria__naam__icontains='badkamers', aantal__gte=min_badkamers)
        eigenschappen_query_grond = PandEigenschap.objects.values_list('pand', flat=True) \
            .filter(eigenschap__naam__icontains='grondopp') \
            .filter(oppervlakte__gte=min_opp) \
            .filter(oppervlakte__lte=max_opp)
        if (criteria_query is [None, '']) or (len(criteria_v) <= 0):
            criteria_query = PandCriteria.objects.values_list('pand', flat=True).filter(criteria__naam__icontains='')

        # Monster query
        panden = Pand.objects.filter(gemeente__icontains=gemeente) \
            .filter(prijs__gte=min_prijs) \
            .filter(prijs__lte=max_prijs) \
            .filter(bouwjaar__gte=bouwjaar) \
            .filter(pk__in=set(criteria_query)) \
            .filter(pk__in=set(aantal_slaapkamers_criteria_query)) \
            .filter(pk__in=set(aantal_badkamers_criteria_query)) \
            .filter(referentienummer__icontains=ref_number) \
            .filter(pk__in=set(eigenschappen_query_grond))
        if get_language() == 'fr':
            panden = panden.filter(staat__naam_fr__icontains=staat).filter(type__naam_fr__icontains=typehuis) \
                .filter(status__naam_fr__icontains=status)
        elif get_language() == 'en':
            panden = panden.filter(staat__naam_en__icontains=staat).filter(type__naam_fr__icontains=typehuis) \
                .filter(status__naam_en__icontains=status)
        else:
            panden = panden.filter(staat__naam__icontains=staat).filter(type__naam__icontains=typehuis) \
                .filter(status__naam__icontains=status)
        context = LoadFooter.get_context(LoadFooter)
        context['alle_panden'] = panden
        return render(request, 'master/panden.html',
                      context)  # {'alle_panden': self.create_pagination(request, panden)}

    def handle_post_request(self, request, status):
        locatie = request.POST.get('locatie').split()
        min_prijs = request.POST.get('min-prijs')
        max_prijs = request.POST.get('max-prijs')
        min_prijs.encode("utf-8")
        max_prijs.encode("utf-8")
        min_prijs = min_prijs.replace(u"\u20ac", "")
        max_prijs = max_prijs.replace(u"\u20ac", "")
        min_prijs.decode("utf-8")
        max_prijs.decode("utf-8")
        min_prijs = min_prijs.replace("+", "").replace(".", "")
        max_prijs = max_prijs.replace("+", "").replace(".", "")
        types = request.POST.get('type-pand').split()
        if min_prijs in [None, ''] or min_prijs.isdigit() == False:
            min_prijs = 0
        if max_prijs in [None, ''] or max_prijs.isdigit() == False:
            max_prijs = 2147000000
        if (len(types) <= 0) or (types in [None, '']):
            types = []
            values = TypeHuis.objects.all()
            for k in values:
                types.append(str(k))
        if len(locatie) > 1:
            gemeente = locatie[1]
            panden = Pand.objects.filter(gemeente__iexact=gemeente).filter(prijs__gte=min_prijs).filter(
                prijs__lte=max_prijs).filter(type__naam__in=types).filter(status__naam__icontains=status)
        else:
            panden = Pand.objects.filter(prijs__gte=min_prijs).filter(
                prijs__lte=max_prijs).filter(type__naam__in=types).filter(status__naam__icontains=status)
        context = LoadFooter.get_context(LoadFooter)
        context['alle_panden'] = panden
        return render(request, 'master/panden.html',
                      context)

    def __init__(self):
        return None


class PandenTeKoop(generic.ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'master/panden.html'
        panden = Pand.objects.filter(status__naam__icontains='koop')
        context = LoadFooter.get_context(LoadFooter)
        context['alle_panden'] = panden
        context['title'] = 'Immo Panden Te Koop op ViaSofie'
        return render(request, template_name, context)

    def post(self, request):
        p = Pand_Main()
        if request.POST.get('search-type') == 'normal':
            return p.handle_post_request(request, 'koop')
        elif request.POST.get('search-type') == 'advanced':
            return p.handle_post_request_advanced(request, 'koop')


class PandenTeHuur(generic.ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'master/panden.html'
        panden = Pand.objects.filter(status__naam__icontains='huur')
        context = LoadFooter.get_context(LoadFooter)
        # context['alle_panden'] = pt.create_pagination(request, panden)
        context['alle_panden'] = panden
        context['title'] = 'Immo Panden Te Huur op ViaSofie'
        return render(request, template_name, context)

    def post(self, request):
        p = Pand_Main()
        if request.POST.get('search-type') == 'normal':
            return p.handle_post_request(request, 'huur')
        elif request.POST.get('search-type') == 'advanced':
            return p.handle_post_request_advanced(request, 'huur')


class PandDetail(generic.DetailView):
    model = Pand
    context_object_name = 'pand'
    template_name = 'master/details.html'

    def get_object(self):
        object = get_object_or_404(Pand, referentienummer=self.kwargs['referentienummer'])
        return object

    def render_to_response(self, context, **response_kwargs):
        response = super(PandDetail, self).render_to_response(context, **response_kwargs)
        context['footer_biv'] = LoadFooter.load_content(LoadFooter)[0]
        context['footer_tel'] = LoadFooter.load_content(LoadFooter)[1]
        context['footer_adres'] = LoadFooter.load_content(LoadFooter)[2]
        context['footer_email'] = LoadFooter.load_content(LoadFooter)[3]
        ip = get_ip(self.request)
        if ip is not None:
            try:
                panden_hit_object = PandHitCount.objects.get(pand=context['pand'], ip=ip)
                panden_hit_object.aantal = panden_hit_object.aantal + 1
                panden_hit_object.unieke_bezoekers = PandHitCount.objects.filter(pand=context['pand']).count()
                panden_hit_object.save()
            except PandHitCount.DoesNotExist:
                PandHitCount.objects.create(pand=context['pand'], ip=ip, aantal=1)
        return response


class IndexView(generic.ListView):
    model = PandHitCount
    context_object_name = 'hitcount'
    template_name = 'master/index.html'

    def loop_add_to_array(self, array, language):
        new_array = []
        for v in array:
            if language == 'fr':
                new_array.append(v.naam_fr)
            elif language == 'en':
                new_array.append(v.naam_en)
            else:
                new_array.append(v.naam)
        return new_array

    @vary_on_headers('User-Agent')
    def get(self, request, *args, **kwargs):
        status = Status.objects.all()
        typehuis = TypeHuis.objects.all()
        criteria = Criteria.objects.all()
        staat = Staat.objects.all()
        array_type = self.loop_add_to_array(typehuis, get_language())
        array_status = self.loop_add_to_array(status, get_language())
        array_criteria = self.loop_add_to_array(criteria, get_language())
        array_staat = self.loop_add_to_array(staat, get_language())


        context = {
            'status': array_status,
            'typehuis': array_type,
            'criteria': array_criteria,
            'staat': array_staat,
            'footer_biv': LoadFooter.load_content(LoadFooter)[0],
            'footer_tel': LoadFooter.load_content(LoadFooter)[1],
            'footer_adres': LoadFooter.load_content(LoadFooter)[2],
            'footer_email': LoadFooter.load_content(LoadFooter)[3]
        };
        return render(request, 'master/index.html', context)

    def post(self, request):
        kijker = Pand.objects.all()
        type = TypeHuis.objects.all()
        pand_eigenschappen = PandEigenschap.objects.all()
        eigenschappen = Eigenschap.objects.all()
        status = Status.objects.all()
        pand_criteria = PandCriteria.objects.all()
        criteria = Criteria.objects.all()
        combined = list(chain(kijker, type, pand_eigenschappen, eigenschappen, status, pand_criteria, criteria))
        data = serializers.serialize('json', combined)
        return HttpResponse(data, content_type="application/json")


class AboutView(View):
    template_name = 'master/about.html'

    def get(self, request):
        context = LoadFooter.get_context(LoadFooter)
        return render(request, self.template_name, context)


class VerkoperView(View):
    form_class = VerkoperForm
    template_name = 'master/verkoper.html'
    subject = ""

    def post(self, request):
        if request.user.is_superuser:
            form = self.form_class(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email")
                username = form.cleaned_data.get("first_name") + '_' + form.cleaned_data.get("last_name")
                existing_email = User.objects.filter(email=email)
                existing_username = User.objects.filter(username=username)
                if not existing_username:
                    if not existing_email:
                        first_name = form.cleaned_data.get("first_name")
                        last_name = form.cleaned_data.get("last_name")
                        username = first_name + '_' + last_name
                        sender = settings.EMAIL_HOST_USER
                        password = User.objects.make_random_password()
                        self.subject = "ViaSofie Account Registratie"
                        html_content = "<center><div style='background-color:#0d3532; border:14px solid black; " \
                                       "color:whitesmoke;padding:40px;'><h1 style='text-align:center;" \
                                       "color:darkseagreen;'>" \
                                       "Jouw inlog gegevens zijn" \
                                       "succesvol aangemaakt!</h1> \n" \
                                       "<p></p>" \
                                       "<p></p>" \
                                       "<p style='text-align:center'>E-mail: " + email + "</p>\n" \
                                        "<p style='text-align:center'>Password: " + password + '</p>' \
                                        "<p></p>" \
                                        "<h2 style='text-align:center'>VIA SOFIE</h2>" \
                                        "</div></center>"
                        msg = EmailMultiAlternatives(self.subject, '', sender, [email])
                        msg.attach_alternative(html_content, "text/html")
                        msg.mixed_subtype = 'related'
                        msg.send()
                        user = User.objects.create_user(username=username, email=email, password=password,
                                                        first_name=first_name, last_name=last_name)
                        context = LoadFooter.get_context(LoadFooter)
                        context['form'] = form
                        context['success'] = 'Account is succesvol aangemaakt! '' \
                        ''De gebruikersnaam & wachtwoord zijn naar ' + \
                                             email + ' verzonden.'
                        return render(request, self.template_name, context)
                    else:
                        context = LoadFooter.get_context(LoadFooter)
                        context['form'] = form
                        context['error'] = 'Dit Email bestaat al!'
                        return render(request, self.template_name, context)
                else:
                    context = LoadFooter.get_context(LoadFooter)
                    context['form'] = form
                    context['error'] = 'De voornaam en achternaam komen overeen met een bestaande gebruiker.'
                    return render(request, self.template_name, context)
        else:
            context = LoadFooter.get_context(LoadFooter)
            context['form'] = form
            context['error'] = 'Formulier fout ingevuld.'
            return render(request, self.template_name, context)
            return render(request, self.template_name, context)

    def get(self, request):
        if request.user.is_superuser:
            context = LoadFooter.get_context(LoadFooter)
            if request.user.is_superuser:
                form = self.form_class(None)
                context['form'] = form
                return render(request, self.template_name, context)
            else:
                return render(request, 'master/index.html', context)
        else:
            return redirect('index')


class AdviceView(View):
    template_name = 'master/advice.html'

    def get(self, request):
        context = LoadFooter.get_context(LoadFooter)
        return render(request, self.template_name, context)


class ProfileView(View):
    def get(self, request):
        context = LoadFooter.get_context(LoadFooter)
        if request.user.is_authenticated():
            return render(request, 'master/profile.html', context)
        else:
            return redirect('index')

    def post(self, request):
        username = request.POST.get('username', '')
        old_password = request.POST.get('old-password', '')
        new_password = request.POST.get('new-password', '')
        new_password_confirmation = request.POST.get('new-password-confirmation', '')
        user = authenticate(username=username, password=old_password)
        if user is not None:
            if new_password == new_password_confirmation:
                user.set_password(new_password)
                user.save()
                return JsonResponse({'success': 'Wachtwoord is succesvol aangepast.'})
            else:
                return JsonResponse({'error': 'Wachtwoorden komen niet overeen!!'})
        else:
            return JsonResponse({'error': 'Huidig wachtwoord klopt niet!'})


class LoginFormView(View):
    form_class = LoginForm
    template_name = 'master/login.html'

    # display bank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # handle submit form
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user_object = User.objects.get(email=email)
                user = authenticate(username=user_object.username, password=password)
                if user is not None:
                    # check if user is banned
                    if user.is_active:
                        login(request, user)
                        return redirect('index')
                else:
                    return JsonResponse({'error': LOGIN_PASSWORD_WRONG_TEXT})
            except ObjectDoesNotExist:
                return JsonResponse({'error': LOGIN_NOT_FOUND_TEXT})
        return JsonResponse({'error': LOGIN_INVALID_FORM_TEXT})


class Loggedin(View):
    template_name = 'master/auth/loggedin.html'

    def get(self, request):
        return render(request, self.template_name)


class Logout(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated():
            logout(request)
        return redirect('index')

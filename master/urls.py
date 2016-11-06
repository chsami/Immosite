from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),  # bij home url doorverwijzen naar index
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^contact/$', views.contact_view, name='contact'),
    url(r'^nieuwsbrief/register/$', views.RegisterNieuwsbrief.as_view(), name='register-nieuwsbrief'),
    url(r'^nieuwsbrief/send/$', views.SendNieuwsbrief.as_view(), name='send-nieuwsbrief'),
    url(r'^nieuwsbrief/activate/(?P<activate_code>[0-9A-Za-z_\-]+)/$', views.ActiveerNieuwsbrief.as_view(), name='activeer-nieuwsbrief'),
    url(r'^verkoper/$', views.VerkoperView.as_view(), name='verkoper'),
    url(r'^advice/$', views.AdviceView.as_view(), name='advice'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^loggedin/$', views.Loggedin.as_view(), name='loggedin'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^disclaimer/$', views.Disclaimer.as_view(), name='disclaimer'),
    url(r'^privacybeleid/$', views.PrivacyBeleid.as_view(), name='privacybeleid'),
    url(r'^sitemap/$', views.SiteMap.as_view(), name='sitemap'),
    url(r'^account/panden/$', views.MijnPanden.as_view(), name='mijn_panden'),

    url(r'^resetpassword/passwordsent/$', views.password_reset_done, name='password_reset_done'),
    url(r'^resetpassword/$', views.password_reset, name='password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),

    url(r'^panden/koop/$', views.PandenTeKoop.as_view(), name='te_koop'),
    url(r'^panden/huur/$', views.PandenTeHuur.as_view(), name='te_huur'),
    url(r'^pand/(?P<referentienummer>[0-9a-z,-_ ]+)/$', views.PandDetail.as_view(), name='pand_detail'),
    url(r'admin-support-ticket/$', views.AdminSupportTicket.as_view(), name='support_ticket'),
    url(r'presearch/$', views.PreSearch.as_view(), name='pre_search'),

]
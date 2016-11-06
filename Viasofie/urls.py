"""Viasofie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static				#check documentatie https://docs.djangoproject.com/en/1.9/howto/static-files/
from django.conf.urls import include, url 				#function allows referencing other URLconfs
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import patterns

admin.site.site_header = 'VIA SOFIE ADMIN'

urlpatterns = patterns('',

    #...#

    (r'^inplaceeditform/', include('inplaceeditform.urls')),

    #...#
)

urlpatterns += i18n_patterns(url(r'^', include('master.urls')), url(r'^inplaceeditform/', include('inplaceeditform.urls')), url(r'^admin/',
   admin.site.urls),)



"""
deze vorm van static mag enkel gerunt worden in development NIET IN PRODUCTION 
if settings.DEBUG:	 zorgt ervoor dat het static enkel gerunt wordt in development 

"""

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)      #root naar mijn static files
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)      #root naar mijn media files

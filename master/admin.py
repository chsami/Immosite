from django.contrib import admin
from .models import Pand
from .models import Criteria, PandCriteria, TypeHuis, Fase, Status, Staat
from .models import PandEigenschap, Eigenschap, Criteria, VerbruiksType, Wettelijk
from .models import VerbruiksType, PandVerbruiksType
from .models import Wettelijk, PandWettelijk, Document, PandDocument
from .models import Bezichtiging, PandBezichtiging, PandHitCount, Nieuwsbrief, \
    DynamicPageContent, DynamicPageContent_EN, DynamicPageContent_FR, MainDynamicPageContent
from .models import Supportticket
from django.shortcuts import get_object_or_404
from master.models import Image


class ImageInlineAdmin(admin.TabularInline):
    model = Image


class CriteriaInlineAdmin(admin.TabularInline):
        model = PandCriteria


class EigenschapInlineAdmin(admin.TabularInline):
    model = PandEigenschap


class VerbruikInlineAdmin(admin.TabularInline):
    model = PandVerbruiksType


class WettelijkInlineAdmin(admin.TabularInline):
    model = PandWettelijk

class DocumentInlineAdmin(admin.TabularInline):
    model = PandDocument

# Panden opties


class PandAdmin(admin.ModelAdmin):
    list_display = ('referentienummer', 'inkijker', 'user', 'fase', 'straat', 'postcode', 'stad', 'prijs', 'profiel_foto_img', 'datum')
    fields = (('referentienummer', 'inkijker'), 'user', ('straat_naam', 'huis_nummer'), ('postcode', 'gemeente'), ('stad', 'land'), ('verdieping', 'aantal_kamers'), 'status', ('staat', 'type', 'fase'), 'bouwjaar', 'prijs',
              'beschrijving', ('profiel_foto', 'plattegrond_gelijksvloer', 'plattegrond_eerste_verdiep'))
    search_fields = ('fase__naam', 'postcode', 'stad')
    list_filter = ['datum']
    inlines = [ImageInlineAdmin, DocumentInlineAdmin, CriteriaInlineAdmin, EigenschapInlineAdmin, VerbruikInlineAdmin, WettelijkInlineAdmin]
    ImageInlineAdmin.can_delete = True
    multiupload_form = True
    multiupload_list = False

    def admin_image(self):
        return '<img src="%s"/>' % self.img

    admin_image.allow_tags = True


class PandCriteriaAdmin(admin.ModelAdmin):
    list_display = ('pand', 'aantal', 'criteria')
    fields = ('pand', ('aantal', 'criteria'))
    search_fields = ('pand__postcode', 'pand__stad', 'criteria__naam')


class PandEigenschapAdmin(admin.ModelAdmin):
    list_display = ('pand', 'eigenschap', 'oppervlakte', 'eenheid')
    search_fields = ('pand__postcode', 'pand__stad', 'eigenschap__naam')


class PandVerbruiksTypeAdmin(admin.ModelAdmin):
    list_display = ('pand', 'verbruik')
    search_fields = ('pand__postcode', 'pand__stad', 'verbruik__naam')


class PandWettelijkAdmin(admin.ModelAdmin):
    list_display = ('pand', 'wettelijk', 'jaartal')
    fields = ('pand', 'wettelijk', ('oppervlakte', 'eenheid'))
    search_fields = ('pand__postcode', 'pand__stad', 'wettelijk__naam')


class PandBezichtigingAdmin(admin.ModelAdmin):
    list_display = ('pand', 'bezichtiging', 'bezichtigd')
    search_fields = ('pand__postcode', 'pand__stad', 'bezichtiging__voornaam_bezoeker',
                     'bezichtiging__achternaam_bezoeker')


class SupportticketAdmin(admin.ModelAdmin):
    list_display = ('user', 'titel', 'beschrijving', 'gemaakt')
    search_fields = ('titel',)


class NieuwsbriefContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'actief',)
    fields = ('email', 'actief',)

class MainDynamicPageContentAdmin(admin.ModelAdmin):
    list_display = ('page_content_nl', 'page_content_en', 'page_content_fr',)

class PandDocumentAdmin(admin.ModelAdmin):
    list_display = ('pand', 'pand_document', 'document_code',)

# Register your models here.

# _________PAND___________
admin.site.register(Pand, PandAdmin)
admin.site.register(TypeHuis)
admin.site.register(Fase)
admin.site.register(Status)
admin.site.register(Staat)
admin.site.register(Eigenschap)
admin.site.register(Criteria)
admin.site.register(VerbruiksType)
admin.site.register(Wettelijk)
admin.site.register(Document)
admin.site.register(PandDocument, PandDocumentAdmin)
admin.site.register(DynamicPageContent)
admin.site.register(DynamicPageContent_FR)
admin.site.register(DynamicPageContent_EN)
# _______BEZICHTIGING__________
admin.site.register(PandBezichtiging, PandBezichtigingAdmin)


#Nieuwsbrief
admin.site.register(Nieuwsbrief, NieuwsbriefContactAdmin)

#CONTENT DYNAMIC LOADING
admin.site.register(MainDynamicPageContent, MainDynamicPageContentAdmin)

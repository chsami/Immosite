#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models import Count
from django.conf import settings
import uuid
from django.core.files.storage import FileSystemStorage

decimal = RegexValidator(r'^[0-9]+(\.[0-9]{1,5})?$', 'Enkel decimalen toegelaten bv. 0.1')
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Enkel alphanumerische waarden toegtelaten bv. abc123  .')
alphaChar = RegexValidator(r'^[a-zA-Zéàë_ ]*$', 'Enkel letters toegelaten bv a-z,A-Z')


class DynamicPageContent(models.Model):

    identifier = models.CharField(unique=True, max_length=140)
    title = models.TextField(blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return str(self.identifier)


class DynamicPageContent_EN(models.Model):

    identifier = models.CharField(unique=True, max_length=140)
    title = models.TextField(blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return str(self.identifier)


class DynamicPageContent_FR(models.Model):

    identifier = models.CharField(unique=True, max_length=140)
    title = models.TextField(blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return str(self.identifier)


class MainDynamicPageContent(models.Model):

    page_content_nl = models.ForeignKey('DynamicPageContent', on_delete=models.CASCADE)
    page_content_en = models.ForeignKey('DynamicPageContent_EN', on_delete=models.CASCADE)
    page_content_fr = models.ForeignKey('DynamicPageContent_FR', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.page_content_nl)


class PandHitCount(models.Model):
    class Meta:
        verbose_name_plural = "Pand hit count's"

    pand = models.ForeignKey('Pand', on_delete=models.CASCADE)
    ip = models.CharField(blank=False, max_length=140)
    unieke_bezoekers = models.SmallIntegerField(default=0)
    aantal = models.SmallIntegerField(default=0)

    def get_unique_clicks(self):
        return PandHitCount.objects.filter(pand=self.pand).count()

    def get_aantal_clicks(self):
        return self.aantal

    def get_pand(self):
        return self.pand

    def __str__(self):
        return str(self.aantal)


class TypeHuis(models.Model):
    class Meta:
        verbose_name_plural = "Pand Type huizen"

    naam = models.CharField(max_length=65, validators=[alphaChar])
    naam_en = models.CharField(max_length=65, validators=[alphaChar])
    naam_fr = models.CharField(max_length=65, validators=[alphaChar])

    def __str__(self):
        return self.naam


class Fase(models.Model):
    class Meta:
        verbose_name_plural = "Pand Fases"

    naam = models.CharField(max_length=15)
    naam_en = models.CharField(max_length=15, validators=[alphaChar])
    naam_fr = models.CharField(max_length=15, validators=[alphaChar])

    def __str__(self):
        return self.naam


class Status(models.Model):
    class Meta:
        verbose_name_plural = "Pand Statussen"

    naam = models.CharField(max_length=65, validators=[alphaChar])
    naam_en = models.CharField(max_length=65, validators=[alphaChar])
    naam_fr = models.CharField(max_length=65, validators=[alphaChar])

    def __str__(self):
        return self.naam

class Staat(models.Model):
    class Meta:
        verbose_name_plural = "Pand Staten"

    naam = models.CharField(max_length=65, validators=[alphaChar])
    naam_en = models.CharField(max_length=65, validators=[alphaChar])
    naam_fr = models.CharField(max_length=65, validators=[alphaChar])

    def __str__(self):
        return self.naam



class Pand(models.Model):
    class Meta:
        verbose_name_plural = "Pand"
        ordering = ["user"]  # sorteren op users

    referentienummer = models.CharField(max_length=255, blank=False, unique=True)
    inkijker = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(TypeHuis, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    staat = models.ForeignKey(Staat, on_delete=models.CASCADE)
    straat_naam = models.CharField(max_length=255, validators=[alphaChar])
    huis_nummer = models.IntegerField()
    stad = models.CharField(max_length=255, validators=[alphaChar])
    gemeente = models.CharField(max_length=255, validators=[alphaChar])
    postcode = models.IntegerField()
    bouwjaar = models.IntegerField(blank=True, null=True)
    prijs = models.PositiveIntegerField()
    beschrijving = models.TextField()
    hits = models.IntegerField(default=0)
    profiel_foto = models.FileField('Profiel_foto', upload_to='media/', default='')
    datum = models.DateField(auto_now_add=True, editable=False)
    aantal_kamers = models.IntegerField()
    land = models.CharField(max_length=255, validators=[alphaChar])
    plattegrond_gelijksvloer = models.FileField('Plattegrond_gelijksvloer', upload_to='media/', default='', blank=True)
    plattegrond_eerste_verdiep = models.FileField('Plattegrond_gelijksvloer', upload_to='media/', default='', blank=True)
    verdieping = models.IntegerField()

    def profiel_foto_img(self):
        return u'<img src="/media_cdn/%s"style="max-width:200px;" />' % self.profiel_foto

    profiel_foto_img.allow_tags = True

    def straat(self):
        return u'%s %s' % (self.straat_naam, self.huis_nummer)
    straat.short_description = "straat"

    def fotos(self):
        alle_fotos = Image.objects.filter(pand=self)
        return alle_fotos

    def criteria(self):
        pand_criterias = PandCriteria.objects.filter(pand=self)
        return pand_criterias

    def eigenschappen(self):
        pand_eigenschappen = PandEigenschap.objects.filter(pand=self)
        return pand_eigenschappen

    def verbruiks_type(self):
        pand_verbruiks_type = PandVerbruiksType.objects.filter(pand=self)
        return pand_verbruiks_type

    def wettelijk(self):
        pand_wettelijk = PandWettelijk.objects.filter(pand=self)
        return pand_wettelijk

    def pand_hit_count(self):
        pand_hitcount = PandHitCount.objects.filter(pand=self)
        return pand_hitcount[0]

    def document(self):
        pand_documenten = PandDocument.objects.filter(pand=self)
        return pand_documenten

    def __str__(self):
        return self.straat_naam + ' ' + str(self.huis_nummer) + ' ' + self.stad + ' ' + str(self.postcode) + ' ' + str(self.type)


class Image(models.Model):
    file = models.FileField('File', upload_to='media/')
    pand = models.ForeignKey('Pand', related_name='images', blank=True, null=True)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.song.storage, self.song.path
        # Delete the model before the file
        super(Image, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)

    def __str__(self):
        return self.file.url


class Criteria(models.Model):
    class Meta:
        verbose_name_plural = "Criteria's"

    naam = models.CharField(max_length=255, validators=[alphaChar], unique=True)
    naam_en = models.CharField(max_length=255, validators=[alphaChar], unique=True)
    naam_fr = models.CharField(max_length=255, validators=[alphaChar], unique=True)

    def __str__(self):
        return self.naam


class PandCriteria(models.Model):
    class Meta:
        unique_together = ("pand", "criteria")
        verbose_name_plural = "Pand criteria's"

    pand = models.ForeignKey(Pand, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    aantal = models.SmallIntegerField(default=1)

    def __str__(self):
        return str(self.pand) + " " + str(self.criteria) + " " + str(self.aantal)

    def get_aantal(self):
        return str(self.aantal)

    def get_criteria(self):
        return str(self.criteria)


class Eigenschap(models.Model):
    class Meta:
        verbose_name_plural = "Eigenschappen"

    naam = models.CharField(max_length=255, validators=[alphaChar], unique=True)
    naam_en = models.CharField(max_length=255, validators=[alphaChar], unique=True)
    naam_fr = models.CharField(max_length=255, validators=[alphaChar], unique=True)

    def __str__(self):
        return self.naam


class PandEigenschap(models.Model):
    class Meta:
        verbose_name_plural = "Pand eigenschappen"

    pand = models.ForeignKey(Pand, on_delete=models.CASCADE)
    eigenschap = models.ForeignKey(Eigenschap, on_delete=models.CASCADE)
    oppervlakte = models.IntegerField(blank=True)
    eenheid = models.CharField(blank=True, max_length=10, default="m")

    def __str__(self):
        return str(self.pand) + ' ' + str(self.eigenschap)


class VerbruiksType(models.Model):
    class Meta:
        verbose_name_plural = "Verbruikstypen"

    naam = models.CharField(max_length=255, validators=[alphaChar], unique=True)

    def __str__(self):
        return self.naam


class PandVerbruiksType(models.Model):
    class Meta:
        verbose_name_plural = "Pand verbruikstypen"

    pand = models.ForeignKey(Pand, on_delete=models.CASCADE)
    verbruik = models.ForeignKey(VerbruiksType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pand) + ' met energievorm ' + str(self.verbruik)


class Wettelijk(models.Model):
    class Meta:
        verbose_name = "wettelijke informatie"
        verbose_name_plural = "Wettelijke informaties"

    naam = models.CharField(max_length=255, validators=[alphaChar], unique=True)

    def __str__(self):
        return self.naam


class PandWettelijk(models.Model):
    class Meta:
        verbose_name_plural = "Wettelijke informaties van panden"

    pand = models.ForeignKey(Pand, on_delete=models.CASCADE)
    wettelijk = models.ForeignKey(Wettelijk, on_delete=models.CASCADE, verbose_name="wettelijke informatie")
    oppervlakte = models.CharField(blank=True, max_length=32, validators=[decimal])
    eenheid = models.CharField(blank=True, max_length=10, default="M")
    jaartal = models.IntegerField()

    def __str__(self):
        return str(self.pand) + ' ' + str(self.wettelijk) + ' ' + str(self.jaartal)


class Document(models.Model):
    class Meta:
        verbose_name_plural = "Documenten"

    naam = models.FileField('Document', upload_to=settings.DOCUMENTEN_URL)

    def __str__(self):
        return str(self.naam)

class PandDocument(models.Model):
    class Meta:
        verbose_name_plural = "Pand Documenten"

    pand = models.ForeignKey(Pand, on_delete=models.CASCADE)
    pand_document = models.ForeignKey(Document, on_delete=models.CASCADE)
    document_code = models.CharField(editable=False, max_length=255, default=uuid.uuid4)

    def __str__(self):
        return "Document : " + str(self.pand_document) + " voor pand " + str(self.pand)


class Bezichtiging(models.Model):
    class Meta:
        verbose_name_plural = "Bezichtigingen"

    voornaam_bezoeker = models.CharField(max_length=255, validators=[alphaChar], verbose_name="Voornaam")
    achternaam_bezoeker = models.CharField(max_length=255, validators=[alphaChar], verbose_name="Achternaam")

    def __str__(self):
        return self.achternaam_bezoeker + ' ' + self.voornaam_bezoeker


class PandBezichtiging(models.Model):
    class Meta:
        verbose_name_plural = "Pand bezichtigingen"
        unique_together = ("pand", "bezichtiging", "datum")  # kan toch niet dat een persoon dezelfde pand meermaals
        # op dezelfde dag bezichtig ofwel?

    pand = models.ForeignKey(Pand, on_delete=models.CASCADE)
    bezichtiging = models.ForeignKey(Bezichtiging, on_delete=models.CASCADE)
    datum = models.DateTimeField()

    def bezichtigd(self):
        return u'%s' % self.datum
    bezichtigd.short_description = "Bezichtigd op"

    def __str__(self):
        return str(self.bezichtiging) + ' ' + str(self.pand) + ' ' + str(self.datum)


class Supportticket(models.Model):
    class Meta:
        verbose_name_plural = "Supporttickets"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titel = models.CharField(max_length=255)
    beschrijving = models.TextField()
    datum = models.DateTimeField()

    def gemaakt(self):
        return u'%s' % self.datum
    gemaakt.short_description = "Gemaakt op"

    def __str__(self):
        return self.titel + ' ' + self.beschrijving + ' ' + str(self.datum)

class Nieuwsbrief(models.Model):
    class Meta:
        verbose_name_plural = "Contacten Nieuwsbrief"

    email = models.EmailField(unique=True, max_length=50, verbose_name="Emailadres")
    actief = models.BooleanField(default=False)
    activate_code = models.CharField(editable=False, max_length=255)

    def __str__(self):
        return str(self.email) + " " + str(self.actief)
from django.db import models
from taggit.managers import TaggableManager


class Document(models.Model):
    file = models.FileField(u"Fichier", max_length=200, upload_to='docs/%Y/%m/%d/')
    title = models.CharField(u"Titre", max_length=200)
    tags = TaggableManager(u"Mots-clés", blank=True, help_text=u"Une liste de mots-clés séparés par des virgules")

    def __str__(self):
        return self.title

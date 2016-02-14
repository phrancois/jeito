from django.db import models


class Document(models.Model):
    file = models.FileField(u"Fichier", max_length=200, upload_to='docs/%Y/%m/%d/')
    title = models.CharField(u"Titre", max_length=200)

    def __str__(self):
        return self.title

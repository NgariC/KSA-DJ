import os

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Doc(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    doc_name = models.CharField('Document name', max_length=200, unique=True)
    file = models.FileField(upload_to='Document/%Y/%m')

    class Meta:
        abstract = True

    @property
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    @property
    def filesize(self):
        x = self.file.size
        y = 512000
        if x < y:
            value = round(x / 1000, 2)
            ext = ' kb'
        elif x < y * 1000:
            value = round(x / 1000000, 2)
            ext = ' Mb'
        else:
            value = round(x / 1000000000, 2)
            ext = ' Gb'
        return str(value) + ext


class Document(Doc):
    description = models.TextField()
    date_to_cease_showing = models.DateField(db_index=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.doc_name


class LegalDocuments(Doc):
    pass

    class Meta:
        ordering = ['doc_name']

    def __str__(self):
        return self.doc_name


class FormTemplate(models.Model):
    name = models.CharField('Form Name', max_length=200)
    file = models.FileField(upload_to='Templates')

    def __str__(self):
        return self.name


@receiver(post_delete, sender=FormTemplate)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)

from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from apps.files.models import Document, LegalDocuments


class DocumentList(LoginRequiredMixin, generic.ListView):
    model = Document
    context_object_name = 'documents'

    def get_queryset(self):
        return Document.objects.filter(date_to_cease_showing__gte=datetime.now().date())


class LegalDocumentsList(LoginRequiredMixin, generic.ListView):
    model = LegalDocuments
    context_object_name = 'legal_documents'

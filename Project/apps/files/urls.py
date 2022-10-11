from django.urls import path

from apps.files import views

app_name = 'files'

urlpatterns = [
    path('documents', views.DocumentList.as_view(), name='downloads'),
    path('legal-documents', views.LegalDocumentsList.as_view(), name='legal_documents'),
]

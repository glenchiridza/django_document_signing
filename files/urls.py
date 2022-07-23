from django.urls import path
from .views import uploadDocument,success_page,sign_document

urlpatterns = [
    path('document/', uploadDocument, name='upload-document'),
    path('', success_page, name='success-page'),
    path('sign/', sign_document, name='sign-document')
]

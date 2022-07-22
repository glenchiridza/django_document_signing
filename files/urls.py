from django.urls import path
from .views import uploadDocument,success_page

urlpatterns = [
    path('document/', uploadDocument, name='upload-document'),
    path('', success_page, name='success-page')
]

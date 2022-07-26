from django.urls import path
from .views import uploadDocument,success_page,sign_document
from . import views
urlpatterns = [

    path('e_list/', views.ESignListView.as_view(), name='list'),
    path('e_create/', views.ESignCreateView.as_view(), name='create'),
    path('e_update/<int:pk>/', views.ESignUpdateView.as_view(), name='update'),
    path('document/', uploadDocument, name='upload-document'),
    path('', success_page, name='success-page'),
    path('send-doc/', views.SendForSigningView.as_view(), name='send-doc'),
    path('sign_send/<int:pk>/', views.sign_send_document, name='sign-send-document'),
    path('sign/', sign_document, name='sign-document'),
    path('esign/', views.esign_document, name='esign-document')
]

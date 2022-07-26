from django.urls import path
from .views import uploadDocument,success_page,sign_document
from . import views
urlpatterns = [

    path('e_list/', views.ESignListView.as_view(), name='list'),
    path('e_create/', views.ESignCreateView.as_view(), name='create'),
    path('e_update/<int:pk>/', views.ESignUpdateView.as_view(), name='update'),
    path('document/', uploadDocument, name='upload-document'),
    path('', success_page, name='success-page'),
    path('sign/', sign_document, name='sign-document')
]

from django.shortcuts import render

from .models import Document

def uploadDocument(request):

    return render(request,'files/files_upload')

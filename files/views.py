from django.shortcuts import render

from .models import Document
from .forms import UploadForm


def uploadDocument(request):
    form = UploadForm()
    if request.method == "POST":
        form

    context = {
        "form": form
    }
    return render(request, 'files/files_upload', context)

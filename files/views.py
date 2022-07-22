from django.shortcuts import render, redirect

from .models import Document
from .forms import UploadForm


def success_page(request):
    documents = Document.objects.all()
    context = {
        "documents": documents
    }
    return render(request, 'files/success.html', context)


def uploadDocument(request):
    form = UploadForm()
    if request.method == "POST":
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success-page")

    context = {
        "form": form
    }
    return render(request, 'files/files_upload.html', context)

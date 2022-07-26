from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Document, Signature, SignDocument, ESignModel, ESignModel
from .forms import UploadForm, SignForm, ESignForm
from .sign_pdf import sign_pdf_file

from django.views import generic


def success_page(request):
    documents = SignDocument.objects.all()
    context = {
        "documents": documents
    }
    return render(request, 'files/success.html', context)


# def sign_uploaded_pdf(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def uploadDocument(request):
    form = UploadForm()
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # instead of save call the method to handle uploaded file
            # sign_uploaded_pdf(request.FILES['file'])
            return redirect("success-page")

    context = {
        "form": form
    }
    return render(request, 'files/files_upload.html', context)


def sign_document(request):
    form = SignForm()
    if request.method == "POST":
        form = SignForm(request.POST)
        if form.is_valid():
            doc_pk = request.POST.get('document')
            sn_pk = request.POST.get('signature')
            page_num = request.POST.get('page_number')
            document = Document.objects.get(id=doc_pk)
            signature = Signature.objects.get(id=sn_pk)
            print(document.upload_pdf.url, signature.signature_image.url)
            full_sign_url = request.build_absolute_uri(signature.signature_image.url)
            sign_pdf_file(document.document_name,
                          str(document.upload_pdf.url)[1:],
                          full_sign_url,
                          int(page_num))
            form.save()
    context = {
        "form": form
    }
    return render(request, 'files/sign_document.html', context)


# Esign views


class ESignCreateView(generic.CreateView):
    model = ESignModel
    fields = '__all__'
    success_url = reverse_lazy('list')


class ESignUpdateView(generic.UpdateView):
    model = ESignModel
    fields = '__all__'
    success_url = reverse_lazy('list')


class ESignListView(generic.ListView):
    model = ESignModel




def sign_document(request):
    form = ESignForm()
    if request.method == "POST":
        form = ESignForm(request.POST)
        if form.is_valid():
            doc_pk = request.POST.get('document')
            sn_pk = request.POST.get('signature')
            page_num = request.POST.get('page_number')
            document = Document.objects.get(id=doc_pk)
            signature = ESignModel.objects.get(id=sn_pk)
            print(document.upload_pdf.url, signature.signature_image.url)
            full_sign_url = request.build_absolute_uri(signature.signature)
            sign_pdf_file(document.document_name,
                          str(document.upload_pdf.url)[1:],
                          full_sign_url,
                          int(page_num))
            form.save()
    context = {
        "form": form
    }
    return render(request, 'files/sign_document.html', context)

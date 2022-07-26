from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from jsignature.templatetags.jsignature_filters import signature_base64
from .models import Document, Signature, SignDocument, ESignModel, ESignModel
from .forms import UploadForm, SignForm, ESignForm
from .sign_pdf import sign_pdf_file
from django.contrib.auth.models import User
from django.views import generic


def success_page(request):
    documents = Document.objects.all()
    signed = []
    not_signed = []
    for doc in documents:
        docs_signed = SignDocument.objects.filter(document__document_name=doc.document_name)
        if docs_signed:
            signed.append(doc)
        else:
            not_signed.append(doc)
    context = {
        "documents": not_signed,
        "signed_docs": signed
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
            num_of_signatures = request.POST.get('num_of_signatures')
            document = Document.objects.get(id=doc_pk)
            signature = Signature.objects.get(id=sn_pk)
            print(document.upload_pdf.url, signature.signature_image.url)
            full_sign_url = request.build_absolute_uri(signature.signature_image.url)

            doc_sign = form.save(commit=False)
            doc_sign.user_signed += 1

            sign_pdf_file(document.document_name,
                          str(document.upload_pdf.url)[1:],
                          full_sign_url,
                          int(page_num),
                          int(num_of_signatures))
            doc_sign.save()
    context = {
        "form": form
    }
    return render(request, 'files/sign_document.html', context)


# Esign views


class ESignCreateView(generic.CreateView):
    model = ESignModel
    fields = ('signature', 'signature_date')
    success_url = reverse_lazy('list')

    def dispatch(self, request, *args, **kwargs):
        exists = User.objects.get(username=self.request.user.username)
        if exists:
            return redirect("/upload/e_update/" + str(self.request.user.id))

    def form_valid(self, form):
        esign = form.save(commit=False)
        esign.user = self.request.user
        esign.save()
        return super(ESignCreateView, self).form_valid(form)


class ESignUpdateView(generic.UpdateView):
    model = ESignModel
    fields = ('signature', 'signature_date')
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        esign = form.save(commit=False)
        esign.user = self.request.user
        esign.save()
        return super(ESignUpdateView, self).form_valid(form)


class ESignListView(generic.ListView):
    model = ESignModel


def esign_document(request):
    form = ESignForm()
    if request.method == "POST":
        form = ESignForm(request.POST)
        if form.is_valid():
            doc_pk = request.POST.get('document')
            sn_pk = request.POST.get('signature')
            page_num = request.POST.get('page_number')
            num_of_signatures = request.POST.get('num_of_signatures')
            document = Document.objects.get(id=doc_pk)
            signature = ESignModel.objects.get(id=sn_pk)
            print(document.upload_pdf.url, signature_base64(signature.signature))
            # full_sign_url = request.build_absolute_uri(signature.signature)
            sign_pdf_file(document.document_name,
                          str(document.upload_pdf.url)[1:],
                          signature_base64(signature.signature),
                          int(page_num),
                          int(num_of_signatures))
            form.save()
    context = {
        "form": form
    }
    return render(request, 'files/sign_document.html', context)

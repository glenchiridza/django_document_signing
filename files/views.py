from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from jsignature.templatetags.jsignature_filters import signature_base64
from .models import Document, Signature, SignDocument, ESignModel, ESignModel, SendForSigning
from .forms import UploadForm, SignForm, ESignForm, SendForSigningForm, SentSignForm
from .sign_pdf import sign_pdf_file
from django.contrib.auth.models import User
from django.views import generic
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def loginPage(request):
    page = 'login'
    # restrict a logged in user from going to the login url again
    if request.user.is_authenticated:
        return redirect('success-page')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User with that username does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('success-page')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {
        'page': page
    }
    return render(request, 'files/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('success-page')


def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('success-page')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {
        'form': form
    }
    return render(request, 'files/login_register.html', context)


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

            doc_sign = form.save(commit=False)
            doc_sign.user_signed = 1

            signature_count = 1
            sign_pdf_file(document.document_name,
                          str(document.upload_pdf.url)[1:],
                          full_sign_url,
                          int(page_num),
                          int(signature_count))
            signed_pdf_link = f"/media/signed_documents/{document.document_name}.pdf"
            doc_sign.signed_document_url = signed_pdf_link
            doc_sign.save()
            return redirect("success-page")

    context = {
        "form": form
    }
    return render(request, 'files/sign_document.html', context)


def sign_send_document(request, pk):
    doc_send = SendForSigning.objects.filter(
        Q(user=request.user) &
        Q(id=pk)
    )
    context = {
        "valid_id": False
    }
    if doc_send:
        form = SentSignForm()
        if request.method == "POST":
            form = SentSignForm(request.POST)
            if form.is_valid():
                sn_pk = request.POST.get('signature')
                page_num = doc_send.document.page_number

                signature = Signature.objects.get(id=sn_pk)

                full_sign_url = request.build_absolute_uri(signature.signature_image.url)

                doc_sign = form.save(commit=False)

                signatures_count = doc_sign.user_signed + 1
                doc_sign.user_signed = doc_send.document.user_signed + 1
                doc_sign.document = doc_send.document.document
                doc_sign.page_number = page_num
                doc_sign.num_of_signatures = doc_send.document.num_of_signatures

                sign_pdf_file(doc_send.document.document_name,
                              str(doc_send.document.upload_pdf.url)[1:],
                              full_sign_url,
                              int(page_num),
                              int(signatures_count))

                doc_sign.signed_document_url = doc_send.document.signed_document_url
                doc_sign.save()
        context = {
            "form": form,
            "items": doc_send,
            "valid_id": True
        }
    return render(request, 'files/sign_existing.html', context)


class SendForSigningView(generic.CreateView):
    template_name = "files/sendforsigning.html"
    form_class = SendForSigningForm

    def form_valid(self, form):
        send = form.save(commit=False)
        send.sender = self.request.user
        send.save()
        return super(SendForSigningView, self).form_valid(form)


class ToBeSigned(generic.ListView):
    template_name = "files/to_be_signed.html"
    queryset = SendForSigning.objects.all()
    context_object_name = "o"


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

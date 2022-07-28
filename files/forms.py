from django.forms import ModelForm
from .models import Document, SignDocument, ESignDocument, SendForSigning


class UploadForm(ModelForm):
    class Meta:
        model = Document
        fields = "__all__"


class SignForm(ModelForm):
    class Meta:
        model = SignDocument
        fields = ("document", "page_number", "num_of_signatures")


class SentSignForm(ModelForm):
    class Meta:
        model = SignDocument
        fields = ("",)


class ESignForm(ModelForm):
    class Meta:
        model = ESignDocument
        fields = ("document", "signature", "page_number", "num_of_signatures")


class SendForSigningForm(ModelForm):
    class Meta:
        model = SendForSigning
        fields = ("receiver","document")

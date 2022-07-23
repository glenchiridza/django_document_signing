from django.forms import ModelForm
from .models import Document,SignDocument


class UploadForm(ModelForm):
    class Meta:
        model = Document
        fields = "__all__"


class SignForm(ModelForm):
    class Meta:
        model = SignDocument
        fields = "__all__"

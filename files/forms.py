from django.forms import ModelForm
from .models import Document,SignDocument,ESignDocument


class UploadForm(ModelForm):
    class Meta:
        model = Document
        fields = "__all__"


class SignForm(ModelForm):
    class Meta:
        model = SignDocument
        fields = "__all__"


class ESignForm(ModelForm):
    class Meta:
        model = ESignDocument
        fields = "__all__"

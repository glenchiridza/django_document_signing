from django.forms import ModelForm
from.models import Document

class UploadForm(ModelForm):
    class Meta:
        model = Document
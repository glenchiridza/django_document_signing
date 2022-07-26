from django.db import models
from jsignature.mixins import JSignatureFieldsMixin
from django.contrib.auth.views import get_user_model

User = get_user_model()


class Signature(models.Model):
    signature_image = models.ImageField(upload_to="signature_image")

    def __str__(self):
        return "signature"


class Document(models.Model):
    document_name = models.CharField(max_length=100)
    upload_pdf = models.FileField(upload_to="pdf_documents")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.document_name


class SignDocument(models.Model):
    document = models.OneToOneField(Document, on_delete=models.SET_NULL, null=True)
    signature = models.OneToOneField(Signature, on_delete=models.SET_NULL, null=True)
    page_number = models.PositiveIntegerField(default=0)
    num_of_signatures = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"signed document {self.document.document_name}"


# jsignature model
class ESignModel(JSignatureFieldsMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class ESignDocument(models.Model):
    document = models.OneToOneField(Document, on_delete=models.SET_NULL, null=True)
    signature = models.OneToOneField(ESignModel, on_delete=models.SET_NULL, null=True)
    page_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"signed document {self.document.document_name}"

from django.db import models


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

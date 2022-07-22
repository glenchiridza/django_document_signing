from django.db import models


class Document(models.Model):
    document_name = models.CharField(max_length=100)
    upload_pdf = models.FileField(upload_to="pdf_documents")

    def __str__(self):
        return self.document_name

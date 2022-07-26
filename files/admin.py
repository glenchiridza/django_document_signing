from django.contrib import admin

from .models import Document, Signature,SignDocument, ESignModel,ESignDocument,SendForSigning

admin.site.register(Signature)
# admin.site.register(SignDocument)
admin.site.register(Document)
admin.site.register(ESignModel)
admin.site.register(ESignDocument)
admin.site.register(SendForSigning)

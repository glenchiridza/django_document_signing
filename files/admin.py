from django.contrib import admin

from .models import Document, Signature,SignDocument

admin.site.register(Signature)
# admin.site.register(SignDocument)
admin.site.register(Document)

from django.contrib import admin

from .models import Document, Signature

admin.site.register(Signature)
admin.site.register(Document)

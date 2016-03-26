from django.contrib import admin
from .models import Feed, Author, Entry

# Register your models here.
admin.register(Feed, Author, Entry)(admin.ModelAdmin)

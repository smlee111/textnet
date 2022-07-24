from django.contrib import admin
from .models import Entity,Synonym

class EntityAdmin(admin.ModelAdmin):
    search_fields = ['value']

class SynonymAdmin(admin.ModelAdmin):
    search_fields = ['value']

admin.site.register(Entity, EntityAdmin)
admin.site.register(Synonym, SynonymAdmin)
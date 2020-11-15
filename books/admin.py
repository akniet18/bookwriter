from django.contrib import admin
from .models import *


@admin.register(Text)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'chapter')
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Track)
admin.site.register(TextOptions)


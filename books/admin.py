from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Text)
admin.site.register(Track)
admin.site.register(TextOptions)


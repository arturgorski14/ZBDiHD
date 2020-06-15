from django.contrib import admin
from .models import *
# Register your models here.

# L: admin
# P: pass1234

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Game)
admin.site.register(ReviewG)

from django.contrib import admin
from .models import *
# Register your models here.

# admin page
# L: admin
# P: pass1234
# cloud
# mongodb+srv://artur:<password>@zbdihd-5qpls.mongodb.net/<dbname>?retryWrites=true&w=majority

# admin.site.register(Movie)
# admin.site.register(Review)
admin.site.register(Game)
admin.site.register(ReviewG)

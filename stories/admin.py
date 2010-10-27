from django.contrib import admin
from models import *

class StoryAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Story, StoryAdmin)
admin.site.register(Genre)

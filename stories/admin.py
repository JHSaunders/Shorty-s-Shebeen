from django.contrib import admin
from models import *

class StoryAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Story, StoryAdmin)
admin.site.register(Genre)

class CompetitionAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('name', 'date','active')
    list_filter = ('date','active')
    search_fields = ['name']
admin.site.register(Competition,CompetitionAdmin)

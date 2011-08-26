from django.contrib import admin
from models import *

class StoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_published'
    list_display = ('author','title','genres','published','hidden','date_published','created','last_updated')
    list_filter = ('published',)
    search_fields = ['title','author__last_name','author__username','author__first_name']

    
admin.site.register(Story)
admin.site.register(Genre)

class CompetitionAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('name', 'date','active')
    list_filter = ('date','active')
    search_fields = ['name']
admin.site.register(Competition,CompetitionAdmin)

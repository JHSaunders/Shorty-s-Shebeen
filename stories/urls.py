from django.conf.urls.defaults import *
import settings
import views

urlpatterns = patterns('',
    url(r'^home$',views.home,name="home"),
    
    url(r'^story/(?P<story_id>\d+)/read',views.read_story,name="read_story"),
    
    url(r'^story/(?P<story_id>\d+)/download',views.download_story,name="download_story"),
    
    url(r'^story/(?P<story_id>\d+)/edit',views.edit_story,name="edit_story"),
    
    url(r'^story/create',views.create_story,name="create_story"),
    
    url(r'^story/random',views.random_story,name="random_story"),
    
    url(r'^story/(?P<story_id>\d+)/rate',views.rate_story,name="rate_story"),
    
    url(r'^archive/$',views.story_archive,name="story_archive"),
    
    url(r'^about/$',views.about,name="about"),
    
    url(r'^search',views.story_archive,name="search"),
    
    url(r'^author/(?P<author_id>\d+)/view',views.view_author,name="view_author"),
    
    url(r'^author/edit_profile', views.edit_profile,name="edit_profile"),
    
    url(r'^author/dashboard', views.author_dashboard,name="author_dashboard"),
    
    url(r'^genre/(?P<genre_id>\d+)/view',views.view_genre, name="view_genre"),
    
    url(r'facebook/test', views.facebook_test),

    url(r'competitions', views.list_competitions, name="competitions"),
)

#Use django to serve static files during development
urlpatterns += patterns('django.views.static',
(r'^media/(?P<path>.*)$', 
    'serve', {
    'document_root': settings.MEDIA_ROOT,
    'show_indexes': True }),)

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import registration

urlpatterns = patterns('',
    # Main Stories App
    (r'^', include('shortys_shebeen.stories.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
#    url(r'^accounts/logout',' django.contrib.auth.views.logout',name="logout_go_home"),
    # Registration    
    (r'^accounts/', include('registration.urls')),
    
    # Comments
    (r'^comments/', include('django.contrib.comments.urls')), 
)

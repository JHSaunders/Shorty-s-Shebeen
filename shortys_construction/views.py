# Create your views here.
from django.views.generic.simple import direct_to_template

def under_construction(req):
    context = {}
    return direct_to_template(req,"shortys_construction/under_construction.html",context)


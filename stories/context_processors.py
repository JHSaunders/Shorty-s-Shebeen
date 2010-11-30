from models import *
def genre_list(req):
  context = {}
  context["genre_list"]=Genre.objects.all()
  return context

import string

from models import *
def genre_list(req):
  context = {}
  context["genre_list"]=Genre.objects.all()
  return context

def detect_user_agent(req):
  user_agent = req.META["HTTP_USER_AGENT"]
  context = {}
  context["user_agent_is_mac"]= string.find(user_agent,"Mac OS X")>-1
  context["user_agent_is_linux"]= string.find(user_agent,"Linux")>-1
  return context

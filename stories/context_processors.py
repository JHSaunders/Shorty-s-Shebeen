import string

from models import *
def genre_list(req):
  context = {}
  context["genre_list"]=Genre.objects.order_by("name")
  return context

def detect_user_agent(req):
  if "HTTP_USER_AGENT" not in req.META:
    return context 
  user_agent = req.META["HTTP_USER_AGENT"]
  context = {}
  context["user_agent_is_mac"]= string.find(user_agent,"Mac OS X")>-1
  context["user_agent_is_linux"]= string.find(user_agent,"Linux")>-1
  return context

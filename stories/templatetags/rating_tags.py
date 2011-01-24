from django import template
from django.utils.safestring import mark_safe
import datetime
import cgi
import random

register = template.Library()

@register.tag
def rating_star_form(parser, token):
    args = token.split_contents()      
    return RatingStarNode(args[1],args[2],args[3].strip('"'),args[4].lower()=="true")

class RatingStarNode(template.Node):
    def __init__(self, number,checked,classes,disabled):
        self.number =number        
        self.checked =checked
                    
        self.classes = classes
        self.disabled = disabled
        
    def render(self, context):
        
        try:
            number = template.Variable(self.number).resolve(context)
        except:
            number =int(self.number)
        
        try:
            rating = template.Variable(self.checked).resolve(context)
            if rating == None:
                checked = 0
            else:
                checked = round(rating)
        except:
            checked =int(self.checked)
        
        s='\n'
        random_name=random.randint(1,1000)
        for n in range(1,number+1):
            s+='<input name ="stars%s" type="radio" class="%s" value="%s" '%(random_name,self.classes,n)
            
            if self.disabled==True:
                s+='disabled="disabled" '
            if n ==checked:
                s+='checked="checked" '
            s+='/>\n'                   
        s+=''
        
        return mark_safe(s)
        

import datetime

from django.db.models import Q
from django.http import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import create_object, update_object, delete_object
from django.views.generic.list_detail import object_detail, object_list
from django.core.urlresolvers import reverse

from django.template.loader import get_template
from django.template import Context

import simplejson
import ho.pisa as pisa
import cStringIO as StringIO
import cgi

from models import *
from forms import *

# This is the ratings forumla for finding the top rated stories
# It balances teh absolute rating against teh amount of votes cast, so a 
# story with one vote of 5/5 wont automatically go to the top
# May want to put in some sort of exponential decay
rating_formula = '((100/%s*rating_score/(rating_votes+%s))+10)/2'

def test(req):
    return HttpResponse("Hello world")

def home(req):
    context = {}

    num_stories = 10
    context["latest"] = Story.published_stories.order_by('-date_published')[:num_stories]    
    context["top_rated"] = Story.published_stories.extra(select={'rating_scorex': 
            rating_formula % 
            (Story.rating.range, Story.rating.weight)}).order_by('-rating_scorex')

    try:
        context["random_story"] = Story.published_stories.order_by('?')[0]
    except:
        context["random_story"] = None
        
    try:
        context["winner_story"] = Competition.objects.filter(judged=True).order_by('-date')[0].winner
    except:
        context["winner_story"] = None
    
    try:
        shorty = User.objects.get(username = "shorty")
        context["shortys_story"] = Story.published_stories.filter(author=shorty).order_by('-date_published')[0]
    except:
        context["shortys_story"] = None
    
    context["genres"] = Genre.objects.all()
    
    return direct_to_template(req,"stories/home.html",context)

def random_story(req):
    context = {}
    context["story"]=Story.published_stories.order_by('?')[0]
    context["do_short_preview"]=True
    return direct_to_template(req,"stories/story_preview.html",context)

@login_required
def edit_story(req,story_id):
    if not Story.objects.get(id=story_id).author == req.user:
        return HttpResponse("Access_Denied")
    return update_object(req,Story,story_id,form_class=StoryForm, post_save_redirect=reverse("read_story",args=[story_id]), template_name="stories/edit_story.html")

@login_required
def create_story(req):
    if req.method=="POST":        
        form = StoryForm(req.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = req.user
            story.save()
            return HttpResponseRedirect(reverse("read_story",args=[story.pk]))
    else:
        form = StoryForm()
    return direct_to_template(req,"stories/edit_story.html",{"form":form})

def read_story(req,story_id):
        story = Story.objects.get(id = story_id)
        if req.user == story.author:
            qs = Story.objects.all()
        else:
            qs = Story.objects.filter(Q(published=True) | Q(hidden=True) )
        
        user_rating = story.rating.get_rating_for_user(req.user, req.META['REMOTE_ADDR'])
        story_rating = round(story.rating.get_rating())
        extra_context = {"next":reverse("read_story",args=[story_id]),
            "user_rating":user_rating,
            "story_rating":story_rating}
            
        return object_detail(req,qs,story_id,template_name="stories/read_story.html",extra_context=extra_context)

def rate_story(req,story_id):
    rating_str = req.GET["rating"]
    if rating_str == "undefined":
        rating = 0
    else:
        rating = int(rating_str)
    
    try:
        if rating>0:
            Story.published_stories.get(id=story_id).rating.add(score=rating, user=req.user, ip_address=req.META['REMOTE_ADDR'])
        else:
            Story.published_stories.get(id=story_id).rating.delete(user=req.user, ip_address=req.META['REMOTE_ADDR'])
    except:
        return HttpResponse("fail")
    
    return HttpResponse("ok")
    
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))

def download_story(req,story_id):
    return render_to_pdf('stories/pdf_story.html',{"object":Story.objects.get(id=story_id)})

def archive(req,template_name,extra_context={}):
    search=req.GET.get("search")
    author=req.GET.get("author")
    genre=req.GET.get("genre")
    year=req.GET.get("year")
    month=req.GET.get("month")
    order=req.GET.get("order","order_date")
    
    context = {}
    context["sidebar"]=True
    context["search"] = search
    context["author"] = author
    context["genre"] = genre
    context["year"] = None if year == None else int(year) 
    context["month"] = None if month == None else int(month)
    context["order"] = order
    context["genres"] = Genre.objects.all()
    for k,v in extra_context.items():
        context[k] = v

    queryset = Story.published_stories.all()
    
    if context["genre"] != None:        
        queryset = queryset.filter(genre__name = context["genre"])
    if context["author"] != None:
        queryset = queryset.filter(author__id = context["author"])
    
    if month !=None:
        next_month = int(month) + 1
        next_year = int(year)
        if next_month == 13:
            next_month = 1
            next_year = next_year + 1
        queryset = queryset.filter(date_published__gte = datetime.date(int(year), int(month),1))
        queryset = queryset.filter(date_published__lt = datetime.date(int(next_year), int(next_month),1))
    elif year != None:
        queryset = queryset.filter(date_published__gte = datetime.date(int(year),1,1))
        queryset = queryset.filter(date_published__lt = datetime.date(int(year)+1,1,1))
    
    if order=="order_rating":
        queryset = queryset.extra(select={'rating_scorex':
            rating_formula % 
            (Story.rating.range, Story.rating.weight)})
        queryset = queryset.order_by('-rating_scorex')
    else:
        queryset = queryset.order_by('-date_published')
        
    years = Story.published_stories.dates('date_published','year')
    months = Story.published_stories.dates('date_published','month')
    
    date_filter = {}
    for year in years:
        date_filter[year.year] = []
    for month in months:
        date_filter[month.year].append(month)
    context["dates"] = date_filter            
    
    return object_list(req,queryset,template_name=template_name, paginate_by=15, template_object_name="story", extra_context=context)

def story_archive(req):
    return archive(req,"stories/story_archive.html");
    
def view_genre(req,genre_id):
    genre_obj = Genre.objects.get(id=genre_id)
    return archive(req,"stories/view_genre.html",{"genre":genre_obj.name,"genre_obj":genre_obj});

def view_author(req,author_id):    
    author_obj = User.objects.get(id=author_id)
    return archive(req,"stories/view_author.html",{"author":author_id,"author_obj":author_obj});
    
def about(req):
    about_title = "About Shorty's Shebeen"
    about_id = Story.objects.filter(author__username="shorty").filter(title=about_title)[0].id
    return read_story(req,about_id)
   
@login_required 
def edit_profile(req):
    profile = req.user.profile
    if req.method=="POST":
        auth_details_form = AuthenticationDetailsForm(req.POST,instance = req.user)
        profile_form = AuthorProfileForm(req.POST,instance = req.user.profile)        
        if auth_details_form.is_valid() and profile_form.is_valid():
            auth_details_form.save()
            profile_form.save()            
    else:
        auth_details_form = AuthenticationDetailsForm(instance = req.user)
        profile_form = AuthorProfileForm(instance = req.user.profile)
    
    return direct_to_template(req,"stories/edit_profile.html",{"auth_details_form":auth_details_form,"profile_form":profile_form})

@login_required
def author_dashboard(req):
    return direct_to_template(req,"stories/dashboard.html",{'story_list':
    Story.objects.filter(author = req.user)})
    
def facebook_test(req):
    import facebook  
    fb = facebook.Facebook(settings.FACEBOOK_API_KEY,settings.FACEBOOK_SECRET_KEY)
    
    req.facebook.stream.publish(
    message = "Test Sample",
    action_links = simplejson.dumps(
        [{'text': "Check Us Out!", 'href': "http://someurl.com"}]),
    target_id = 'nf')
    
    return test(req)
    
def list_competitions(req):
   return direct_to_template(req,"stories/competitions_list.html",{'open_competitions':
    Competition.objects.filter(active=True),'closed_competitions':
    Competition.objects.filter(judged=True)})
    

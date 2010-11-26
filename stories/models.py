import datetime
import popularity

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from djangoratings.fields import AnonymousRatingField

class PublishedStoryManager(models.Manager):
        def get_query_set(self):
            return super(PublishedStoryManager, self).get_query_set().filter(published=True)

class Story(models.Model):
    """
        The Story Model:
        + Provides custom manager to only get published stories
        + Automatically updates publication date
        + A Preview function which gives the first
    """
    class Meta:
        verbose_name_plural = "stories"   
    
    author = models.ForeignKey(User,related_name = 'stories',editable=False)
    title = models.CharField(max_length = 100)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    last_updated = models.DateTimeField(auto_now = True)
    tags = models.CharField(max_length = 100,blank=True)
    genre = models.ManyToManyField('Genre', related_name = 'stories')
    
    rating = AnonymousRatingField(range=5,can_change_vote = True, allow_anonymous=True)
    
    published = models.BooleanField()
    date_published = models.DateTimeField(editable = False,null=True)
    
    objects = models.Manager()
    published_stories = PublishedStoryManager()
      
    def __unicode__(self):
        return self.title   
    
    def save(self):
        
        if self.published ==True and self.date_published == None:
            self.date_published = datetime.datetime.now()
             
        super(Story, self).save()
    
    @property        
    def preview(self):
        preview_size = 800
        end = min(preview_size,len(self.text))
        return self.text[0:end-1].strip()+'...'
    
    @property       
    def short_preview(self):
        preview_size = 200
        end = min(preview_size,len(self.text))
        return self.text[0:end-1].strip()+'...'
    
    @property
    def genres(self):        
        first = True
        s=""        
        for g in self.genre.all():
            if not first:
                s=s+", "
            first = False
            s=s+g.name
        return s
    
popularity.register(Story)
    
class Genre(models.Model):
    name = models.CharField(max_length = 100)
    
    def __unicode__(self):
        return self.name

class AuthorProfile(models.Model):
    user = models.OneToOneField(User,editable=False)
    about = models.TextField(blank=True)
    website = models.URLField(default="",blank=True)
    blog = models.URLField(default="",blank=True)

def user_unicode(self):
    if self.first_name !="":
        return "%s %s"%(self.first_name,self.last_name)
    else:
        return self.username

def user_get_or_create_profile(self):
    try:
        return self.get_profile()
    except Exception as e:
        print e
        profile = AuthorProfile(user=self)
        profile.save()
        return profile

User.__unicode__= user_unicode
User.profile = property(user_get_or_create_profile)

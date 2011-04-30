from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed
from django.contrib.syndication.views import FeedDoesNotExist
from django.shortcuts import get_object_or_404
from models import *

from views import rating_formula

class GenreFeed(Feed):
    def get_object(self, request, genre_id):
        return Genre.objects.get(id = genre_id)

    def title(self, obj):
        return "%s stories from Shorty's Short Story Shebeen" % obj.name

    def link(self, obj):
        return reverse("genre_feed",args=[obj.id])

    def description(self, obj):
        return "%s stories from Shorty's Short Story Shebeen" % obj.name

    def items(self, obj):
        return Story.published_stories.filter(genre=obj)[:30]
        
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return item.get_absolute_url()

class AuthorFeed(Feed):
    def get_object(self, request, author_id):
        return User.objects.get(id = author_id)

    def title(self, obj):
        return "Stories by %s from Shorty's Short Story Shebeen" % obj

    def link(self, obj):
        return reverse("genre_feed",args=[obj.id])

    def description(self, obj):
        return "Stories by %s from Shorty's Short Story Shebeen" % obj

    def items(self, obj):
        return Story.published_stories.filter(author=obj)[:30]
        
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return item.get_absolute_url()
        
class LatestFeed(Feed):
    def title(self):
        return "Latest stories from Shorty's Short Story Shebeen"

    def link(self):
        return reverse("latest_feed")

    def description(self):
        return "Latest stories from Shorty's Short Story Shebeen"

    def items(self):
        return Story.published_stories.all()[:30]
        
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return item.get_absolute_url()
        
class TopRatedFeed(Feed):
    def title(self):
        return "Top rated stories from Shorty's Short Story Shebeen"

    def link(self):
        return reverse("top_rated_feed")

    def description(self):
        return "Top rated stories from Shorty's Short Story Shebeen"

    def items(self):
        return Story.published_stories.extra(select={'rating_scorex': 
            rating_formula % 
            (Story.rating.range, Story.rating.weight)}).order_by('-rating_scorex')[:10]
        
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return item.get_absolute_url()

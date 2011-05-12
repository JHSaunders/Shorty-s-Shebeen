from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed
from django.contrib.syndication.views import FeedDoesNotExist
from django.shortcuts import get_object_or_404
from models import *

from views import rating_formula
import markdown

class StoryFeed(Feed):
    title_template = "stories/feed_item_title.html"
    description_template = "stories/feed_item_description.html"
    
#    def item_title(self, item):
#        return "{0} by <i>{1}</i>".format(item.title,item.author)

#    def item_description(self, item):
#        md = markdown.Markdown(safe_mode="replace")
#        text = item.text#item.get_preview(1000)
#        html = md.convert(text)
#        return html
#    
    def item_link(self, item):
        return item.get_absolute_url()

class GenreFeed(StoryFeed):
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
    
class AuthorFeed(StoryFeed):
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
    
class LatestFeed(StoryFeed):
    def title(self):
        return "Latest stories from Shorty's Short Story Shebeen"

    def link(self):
        return reverse("latest_feed")

    def description(self):
        return "Latest stories from Shorty's Short Story Shebeen"

    def items(self):
        return Story.published_stories.all()[:30]
    
class TopRatedFeed(StoryFeed):
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
            

from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


# simple tag
@register.simple_tag
def total_posts():
    return Post.published.count()

# inclusion tag
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.inclusion_tag('blog/post/archive.html')
def archive():
	list_years = []
	posts = Post.published.all()
	for post in posts:
		list_years.append(post.publish.year)
	list_years = list(set(list_years))
	return {'posts': list_years}

@register.inclusion_tag('blog/post/tag_list.html')
def tag_list():
	tags = Post.tags.all()
	repeatation = tags.annotate(num_times=Count('taggit_taggeditem_items'))

	return {'tags': tags, 'tag_dict': repeatation}
	

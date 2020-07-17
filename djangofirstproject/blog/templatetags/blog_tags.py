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


@register.simple_tag
def xrange():
    first_post = Post.published.all().order_by('publish')[:1]
    for p in first_post:
        first_post_year = p.publish.year

    last_post = Post.published.all().order_by('-publish')[:1]
    for p in last_post:
        last_post_year = p.publish.year
    holder = []
    for n in range(first_post_year, last_post_year+1):
        holder.append(n)
    return holder

@register.simple_tag
def first_year():
    first_post = Post.published.all().order_by('publish')[:1]
    for p in first_post:
        first_post_year = p.publish.year
    return first_post_year

@register.simple_tag
def last_year():
    last_post = Post.published.all().order_by('-publish')[:1]
    for p in last_post:
        last_post_year = p.publish.year
    return last_post_year

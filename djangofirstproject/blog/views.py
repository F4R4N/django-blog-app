from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Subscriber
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm, News
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
import os

my_email = os.environ.get('PTSEENV')

def post_list(request, tag_slug=None, year_archive=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    if year_archive:
        object_list = object_list.filter(publish__year=year_archive)

    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # posts = Post.published.all()

    return render(request, 'blog/post/list.html',
                  {'page': page, 'posts': posts, 'tag': tag, 'paginator': paginator, 'year': year_archive})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"read {post.title} at {post_url}\n\n{cd['name']}\'s shared this post and sayed: {cd['comments']}"
            send_mail(subject, message, my_email, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # results = Post.published.annotate(similarity=TrigramSimilarity('title', query), ).filter(similarity__gt=0.1).order_by('-similarity')
            results = Post.published.filter(title__contains=query) or Post.published.filter(body__contains=query) or Post.published.filter(author__username__contains=query)
    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    post.visits = post.visits + 1
    post.save()

    comments = post.comments.filter(active=True)
    new_comment = None
    
    if request.method == 'POST':
    	comment_form = CommentForm(data=request.POST)
    	if comment_form.is_valid():
    		new_comment = comment_form.save(commit=False)
    		new_comment.post = post
    		new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts, })


def newsletter(request):
    new_user = None
    if request.method == 'POST':
        signin_form = News(data=request.POST)
        if signin_form.is_valid():
            new_user = signin_form.save(commit=False)
            signin_form.save()
            name = signin_form.cleaned_data.get('name')
            last_name = signin_form.cleaned_data.get('last_name')
            email = signin_form.cleaned_data.get('email')

    # subscriber = Subscriber.active.all()

    else:
        signin_form = News()
    return render(request, 'blog/post/newsletter.html', {'register_form': signin_form})

def archive(request):
    post = Post.published.all()
    container = []
    for p in post:
        container.append(p.publish.year)
    container = list(set(container))
    return render(request, 'blog/post/archive.html', {'years': container})




# def like(request):
#     if request.method == 'POST':
#         slug = request.POST.get('slug', None)
#         post = get_object_or_404(Post, slug=slug)

#         if post.likes.filter(id=)
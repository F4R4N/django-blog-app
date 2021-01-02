from django.urls import path, re_path
from django.conf.urls import url
from . import views
from .feeds import LatestPostFeed

from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('newsletter/', views.newsletter, name='news_letter'),
    path('archive/<int:year_archive>', views.post_list, name='archive'),
    # path('like/', views.like, name='like'),
    
    # path('search/', views.post_list, name='search')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from django.conf.urls import url
from . import views
from .feeds import LatestPostFeed
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


]

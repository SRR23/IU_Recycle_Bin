
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('list/', post_list, name="post_list"),
    path('post/<str:slug>/', post_details, name="post_details"),
    path('add_reply/<int:blog_id>/<int:comment_id>/', add_reply, name='add_reply'),
    path('search_posts/', search_posts, name='search_posts'),
]
from django.urls import path
from .views import *
urlpatterns = [
    path('category_post/<str:slug>/', category_post, name='category_post'),
]
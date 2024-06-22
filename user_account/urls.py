from django.urls import path
from .views import *

urlpatterns = [
    path('login/',login_user,name='login_user'),
    path('profile/', profile, name='profile'),
    path('add_post/', add_blog, name='add_blog'),
    path('my_post/', my_post, name='my_post'),
    path('update_post/<str:slug>/', update_post, name='update_post'),
    path('register_user/', register_user, name='register_user'),
    path('logout/', logout_user, name='logout_user'),
    path('view_author_information/<str:username>/', view_user_information, name="view_user_information"),
]
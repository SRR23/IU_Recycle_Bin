
from django.urls import path, include
from .views import *

urlpatterns = [
    path('contact_admin/', contact, name="contact"),
    
]
from django.db import models
from category.models import Category
from tag.models import Tag
from user_account.models import User
from .slug import generate_unique_slug
from tinymce.models import HTMLField  
# Create your models here.

class Blog(models.Model):
    user=models.ForeignKey(User, related_name='user_blogs', on_delete=models.CASCADE)
    category=models.ForeignKey(Category, related_name='category_blogs', on_delete=models.CASCADE)
    tags=models.ManyToManyField(Tag,related_name='tag_blogs',blank=True)
    title=models.CharField(max_length=250)
    availability=models.CharField(max_length=250, default="")
    slug=models.SlugField(null=True, blank=True)
    banner=models.ImageField(upload_to='blog_banners')
    description=HTMLField() 
    created_date=models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self,*args,**kwargs):
        updating = self.pk is not None
        
        if updating:
            self.slug = generate_unique_slug(self, self.title, update=True)
            super().save(*args, **kwargs)
        else:
            self.slug=generate_unique_slug(self,self.title)
            super().save(*args,**kwargs)

from django.db import models
from user_account.models import User
from blog.models import Blog

# Create your models here.

class Comment(models.Model):
    user=models.ForeignKey(User,related_name='user_comment',on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,related_name='blog_comment',on_delete=models.CASCADE)
    comment=models.TextField(max_length=250)
    created_date=models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return self.comment


class Reply(models.Model):
    user=models.ForeignKey(User,related_name='user_replies',on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,related_name='comment_replies',on_delete=models.CASCADE)
    text=models.TextField()
    created_date=models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return self.text
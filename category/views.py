from django.shortcuts import render
from blog.models import Blog
from tag.models import Tag
from .models import Category
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
# Create your views here.

def category_post(request, slug):
    category = get_object_or_404(Category, slug=slug)
    query = category.category_blogs.all()
    tags = Tag.objects.order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(query, 2)
    all_blogs = Blog.objects.order_by('-created_date')
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('post_list')

    context = {
        "blogs": blogs,
        "tags": tags,
        "all_blogs": all_blogs
    }
    return render(request, 'category_post.html', context)

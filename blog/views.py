from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from tag.models import Tag
from .forms import TextForm
from category.models import Category
from review.models import Comment, Reply
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def home(request):
    posts=Blog.objects.order_by('-created_date')
    tags=Tag.objects.order_by('-created_date')
    
    context={
        "posts":posts,
        'tags':tags,
    }
    
    return render(request, 'home.html', context)


def post_details(request, slug):
    # this 'blog' is used in post_details.html
    form=TextForm()
    blog=get_object_or_404(Blog, slug=slug)
    category = Category.objects.get(id=blog.category.id)
    related_blogs = category.category_blogs.all()
    tags=Tag.objects.order_by('-created_date')
    
    if request.method == "POST" and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('message')
            Comment.objects.create(
                user=request.user,
                blog=blog,
                comment=comment,
            )
            
            return redirect('post_details', slug=slug)
    
    context={
        "blog":blog,
        'tags':tags,
        "related_blogs": related_blogs,
        "form":form
    }
    
    return render(request, 'post_details.html', context)


def post_list(request):
    posts=Blog.objects.order_by('-created_date')
    tags=Tag.objects.order_by('-created_date')
    page=request.GET.get('page', 1)
    paginator=Paginator(posts,6)
    
    try:
        blogs=paginator.page(page)
    except EmptyPage:
        blogs=paginator.page(1)
    except PageNotAnInteger:
        blogs=paginator.page(1)
        return redirect('post_list')
        
    context={
    "blogs":blogs, 
    "tags":tags, 
    "paginator":paginator
    }
    return render(request, 'post_list.html', context)


@login_required(login_url='login_user')
def add_reply(request, blog_id, comment_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(
                user=request.user,
                comment=comment,
                text=form.cleaned_data.get('message')
            )
    return redirect('post_details', slug=blog.slug)



def search_posts(request):
    search_key = request.GET.get('query', None)
    tags = Tag.objects.order_by('-created_date')
    
    if search_key:
        blogs = Blog.objects.filter(
            Q(title__icontains=search_key) |
            Q(category__title__icontains=search_key) |
            Q(user__username__icontains=search_key) |
            Q(tags__title__icontains=search_key)
        ).distinct()
        
        if not blogs.exists():
            messages.info(request, f'No results found for "{search_key}".')
            
        context = {
            "blogs": blogs,
            "tags": tags,
            "search_key": search_key, 
        }
        
        return render(request, 'search_posts.html', context)

    else:
        return redirect('home')
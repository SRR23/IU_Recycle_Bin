from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, UserRegistrationForm, UserProfileUpdateForm, AddBlogForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.utils.encoding import force_bytes, force_str
from .models import User
from tag.models import Tag
from category.models import Category
from blog.models import Blog
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views.decorators.cache import never_cache
from .decorator import not_logged_in_required
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

# Create your views here.
@never_cache
@not_logged_in_required
def login_user(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
            
                return redirect('home')
            else:
                messages.warning(request, "Sorry, You haven't registered yet")

    context = {
        "form": form
    }
    return render(request, 'login.html', context)


@never_cache
@not_logged_in_required
def register_user(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "Registration successful, Please login")
            return redirect('login_user')

    context = {
        "form": form
    }
    return render(request, 'registration.html', context)



def logout_user(request):
    logout(request)
    return redirect('login_user')

@login_required(login_url='login_user')
def profile(request):
    account = get_object_or_404(User, pk=request.user.pk)
    form = UserProfileUpdateForm(instance=account)
    
    if request.method == "POST":
        if request.user.pk != account.pk:
            return redirect('home')
        
        form = UserProfileUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated successfully")
            return redirect('profile')
        else:
            print(form.errors)

    context = {
        "account": account,
        "form": form
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login_user')
def add_blog(request):
    form = AddBlogForm()

    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            # description = request.POST['description']
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            blog.category = category
            # blog.description = description
            blog.save()

            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)

            messages.success(request, "Post added successfully")
            return redirect('post_details', slug=blog.slug)
        else:
            print(form.errors)

    context = {
        "form": form
    }
    return render(request, 'add_post.html', context)


@login_required(login_url='login')
def my_post(request):
    queryset = request.user.user_blogs.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 6)
    delete = request.GET.get('delete', None)

    if delete:
        blog = get_object_or_404(Blog, pk=delete)
        
        if request.user.pk != blog.user.pk:
            return redirect('home')

        blog.delete()
        messages.success(request, "Your post has been deleted!")
        return redirect('my_post')

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "paginator": paginator
    }
    
    return render(request, 'my_post.html', context)


@login_required(login_url='login')
def update_post(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    form = AddBlogForm(instance=blog)

    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES, instance=blog)
        
        if form.is_valid():
            
            if request.user.pk != blog.user.pk:
                return redirect('home')
            
            existing_tags = blog.tags.all()  # Store existing tags

            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            blog.category = category
            
           
            blog.save()

            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)
            
            for tag in existing_tags:
                if tag.title not in [t.strip() for t in tags]:
                    blog.tags.remove(tag)

            messages.success(request, "Post updated successfully")
            return redirect('post_details', slug=blog.slug)
        else:
            print(form.errors)


    context = {
        "form": form,
        "blog": blog
    }
    return render(request, 'update_post.html', context)



def view_user_information(request, username):
    account = get_object_or_404(User, username=username)

    if request.user.is_authenticated:
        
        if request.user.id == account.id:
            return redirect("profile")

    context = {
        "account": account,
    }
    return render(request, "author_information.html", context)
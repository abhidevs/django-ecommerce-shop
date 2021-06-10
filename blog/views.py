from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Post
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import AddPostForm
import html2text
import json
from django.template.defaultfilters import slugify


def index(request):
    posts = Post.objects.all().filter(draft_status=False).order_by('-post_date')
    text_maker = html2text.HTML2Text()
    for post in posts:
        text_maker.ignore_links = True
        text_maker.ignore_tables = True
        text_maker.ignore_images = True
        text_maker.ignore_anchors = True
        text_maker.ignore_emphasis = True
        text_maker.unicode_snob = True
        post.content = text_maker.handle(post.content)
        post.content = post.content.replace('#', '').strip()
    params = {'posts': posts}
    return render(request, 'blog/index.html', params)


def detailedPost(request, slug):
    post = Post.objects.filter(slug=slug)[0]
    params = {'post': post}
    return render(request, 'blog/detailedPost.html', params)


def search(request):
    query = request.GET['query']
    if len(query) > 78:
        posts = []
    else:
        matchedTitle = Post.objects.filter(draft_status=False, title__icontains=query)
        matchedContent = Post.objects.filter(draft_status=False, content__icontains=query)
        posts = matchedTitle.union(matchedContent)

        text_maker = html2text.HTML2Text()
        for post in posts:
            text_maker.ignore_links = True
            text_maker.ignore_tables = True
            text_maker.ignore_images = True
            text_maker.ignore_anchors = True
            text_maker.ignore_emphasis = True
            text_maker.unicode_snob = True
            post.content = text_maker.handle(post.content)
            post.content = post.content.replace('#', '').strip()

    params = {'posts': posts , 'query': query}
    return render(request, 'blog/search.html', params)


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = User.objects.create_user(username, email, password)
        user.save()
        login(request, user)
        
        if user.has_perm('blog.blog_editor_status'):
            return redirect('dashboard')
        else:
            return redirect('/blog/')
    else:
        params = {}
        return render(request, 'blog/signup.html', params)


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if user.has_perm('blog.blog_editor_status'):
                return redirect('dashboard')
            else:
                return redirect('/blog/')
        else:
            return render(request, 'blog/login.html', {'loginFailure': True})
    else:
        params = {}
        return render(request, 'blog/login.html', params)


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('/blog/')



def dashboard(request):
    if request.user.is_authenticated and request.user.has_perm('blog.blog_editor_status'):
        posts = Post.objects.all().order_by('-post_date')
        params = {'posts': posts}
        return render(request, 'blog/dashboard.html', params)
    else:
        return redirect('/blog/')


def addPost(request):
    if request.user.is_authenticated and request.user.has_perm('blog.blog_editor_status'):
        if request.method == 'POST':
            form = AddPostForm(request.POST, request.FILES)
            if form.is_valid():
                post =  form.save()
                params = {'post_id': post.post_id , 'post_slug': slugify(post.title)}
                return JsonResponse(params, status=200)
            else:
                err = next(iter(form.errors.as_data())) + ' is required.'
                params = {'error': err}
                return JsonResponse(params, status=200)
        else:
            form = AddPostForm()
            params = {'form': form}
            return render(request, 'blog/addPost.html', params)
    else:
        return redirect('/blog/')


def editPost(request, action, post_id):
    if request.user.is_authenticated and request.user.has_perm('blog.blog_editor_status'):
        if request.method == 'POST':
            if action == 'edit':
                title = request.POST['title']
                content = request.POST['content']
                category = request.POST['category']
                author = request.POST['author']
                post_id = post_id[1:]

                post = Post.objects.filter(post_id=post_id)[0]
                post.title = title
                post.category = category
                post.author = author
                post.content = content

                if 'image' in request.FILES:
                    post.image = request.FILES['image']
                post.save()

                params = {'post_slug': slugify(post.title)}
                return JsonResponse(params, status=200)
            elif action == 'publish':
                post_id = post_id[1:]
                post = Post.objects.filter(post_id=post_id).update(draft_status=False)

                params = {}
                return JsonResponse(params, status=200)
            elif action == 'toDraft':
                post_id = post_id[1:]
                post = Post.objects.filter(post_id=post_id).update(draft_status=True)

                params = {}
                return JsonResponse(params, status=200)

        else:
            post = Post.objects.filter(post_id=post_id[1:])[0]
            form = AddPostForm(instance=post)
            params = {'form': form, 'post': post}
            return render(request, 'blog/editPost.html', params)
    else:
        return redirect('/blog/')


def deletePost(request, post_id):
    if request.user.is_authenticated and request.user.has_perm('blog.blog_editor_status'):
        Post.objects.filter(post_id=post_id[1:]).delete()

        params = {}
        return render(request, 'blog/editPost.html', params)
    else:
        return redirect('/blog/')

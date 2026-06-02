from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Post, Comment, Profile
from .forms import PostForm, CommentForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import markdown


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {
        'form': form
    })

def post_list(request):
    query = request.GET.get('q')
    posts = Post.objects.all().order_by('-created_at')

    if query:
        posts = posts.filter(
            title__icontains=query
        ) | Post.objects.filter(
            body__icontains=query
        )

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/post_list.html', {
        'page_obj': page_obj,
        'query': query,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('-created_at')
    comment_form = CommentForm()

    html_body = markdown.markdown(
        post.body,
        extensions=[
            'fenced_code',
            'codehilite',
        ]
    )

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'html_body': html_body,
        'comments': comments,
        'comment_form': comment_form,
    })


def post_category(request, category):
    posts = Post.objects.filter(category=category).order_by('-created_at')

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/post_list.html', {'page_obj': page_obj})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {'form': form})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {'form': form})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'posts/post_confirm_delete.html', {'post': post})


@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect('post_detail', slug=post.slug)


@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('profile_detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'registration/profile_form.html', {
        'form': form
    })


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)

    return render(request, 'registration/profile_detail.html', {
        'profile_user': user,
        'profile': profile
    })
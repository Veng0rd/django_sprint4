from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from blog.forms import CommentForm, PostForm, UserUpdateForm
from blog.models import Comment, Post, Category
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from blog.utils import get_current_user, user_allow

app_name = 'blog'
User = get_user_model()


def index(request):
    template = 'blog/index.html'
    current_time = timezone.now()
    posts = Post.objects.select_related(
        'category', 'author', 'location',
    ).filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    )
    for post in posts:
        post.comment_count = Comment.objects.filter(post=post).count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'post_list': posts,
        'page_obj': page_obj
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    current_user = get_current_user(request)
    current_time = timezone.now()
    post = get_object_or_404(
        Post,
        Q(pub_date__lte=current_time) | Q(author=current_user),
        Q(is_published=True) | Q(author=current_user),
        Q(category__is_published=True) | Q(author=current_user),
        pk=post_id
    )
    print(post.image)
    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'form': CommentForm(),
        'comments': comments
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    current_time = timezone.now()
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    posts = Post.objects.select_related(
        'category', 'author', 'location'
    ).filter(
        pub_date__lte=current_time,
        is_published=True,
        category=category
    )
    print(posts)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    for post in posts:
        post.comment_count = Comment.objects.filter(post=post).count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': user,
        'page_obj': page_obj
    }
    return render(request, template, context)


def edit_profile(request):
    template = 'blog/user.html'
    instance = get_object_or_404(get_user_model(), pk=request.user.id)
    form = UserUpdateForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=form.cleaned_data['username'])
    context = {
        'form': form
    }
    return render(request, template, context)


@login_required
def create_post(request):
    template = 'blog/create.html'
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        user = request.user
        instance = form.save(commit=False)
        instance.author = user
        instance.save()
        return redirect('blog:profile', username=user.username)
    context = {
        'form': form
    }
    return render(request, template, context)


def edit_post(request, post_id):
    template = 'blog/create.html'
    user = request.user
    instance = get_object_or_404(Post, pk=post_id)
    if not user_allow(request, instance.author.id):
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('blog:profile', username=user.username)
    context = {
        'form': form
    }
    return render(request, template, context)


@login_required
def delete_post(request, post_id):
    template = 'blog/create.html'
    user = request.user
    instance = get_object_or_404(Post, pk=post_id)
    if not user_allow(request, instance.author.id):
        return redirect('blog:profile', username=user.username)
    form = PostForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:profile', username=user.username)
    context = {
        'form': form
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        post.comment_count += 1
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    template = 'blog/create.html'
    instance = get_object_or_404(Comment, pk=comment_id)
    if not user_allow(request, instance.author.id):
        return redirect('blog:post_detail', post_id=post_id)
    form = CommentForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('blog:post_detail', post_id=post_id)
    context = {
        'form': form
    }
    return render(request, template, context)


@login_required
def delete_comment(request, post_id, comment_id):
    template = 'blog/comment.html'
    user = request.user
    instance = get_object_or_404(Comment, pk=comment_id)
    if not user_allow(request, instance.author.id):
        return redirect('blog:profile', username=user.username)
    if request.method == 'POST':
        instance.delete()
        success_url = reverse_lazy('blog:index')
        return redirect(success_url)
    context = {
        'comment': instance
    }
    return render(request, template, context)
